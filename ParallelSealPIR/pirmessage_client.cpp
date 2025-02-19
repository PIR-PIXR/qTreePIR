#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <fstream>
#include <thread>
#include <mutex>
#include <grpcpp/grpcpp.h>
#include <condition_variable>
#include "proto/pirmessage.grpc.pb.h"
#include "pir.hpp"
#include "pir_client.hpp"
#include "helper.hpp"
#include "safequeue.hpp"
#include "/home/nhat/Desktop/vcpkg/installed/x64-linux/include/rapidjson/document.h"
//#include "/home/dowload/vcpkg/installed/x64-linux/include/rapidjson/document.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using pir_message::PIRService;
using pir_message::RequestData;
using pir_message::ResponseData;
using pir_message::DBInfoRequest;

using namespace std;
using namespace seal;
using namespace rapidjson;
using namespace std::chrono;

#define CLIENT_LOG_FILE  "client_log.txt"

void clientLogResult(fstream *f, ClientResultLog* Log);

fstream fLogfile;

class ClientWorker {
public:
  ClientWorker(std::shared_ptr<Channel> channel)
  : stub_(PIRService::NewStub(channel)) {}

  ClientWorker(std::shared_ptr<Channel> channel,std::string jsfile,uint64_t eIndex)
  : stub_(PIRService::NewStub(channel)),jsonDBFileName(jsfile),ele_index(eIndex) {}

  int GetDBInfo(pir_message::DBInfo &dbInfo) {
    ClientContext context;
    DBInfoRequest requestDB;
    requestDB.set_dbname(jsonDBFileName);
    Status status =  stub_->GetDBInfo(&context, requestDB, &dbInfo);
    if (status.ok()) {
      //Log.Size = dbInfo.num_of_items();
      return 0;
    }
    else {
      return -1;
    }
  }

  // Assembles the client's payload, sends it and presents the response back
  // from the server.
  std::string GetPIRAnsFromServer(PIRClient *pirClient, const RequestData& request, int num_servers) {
    ResponseData reply;
    ClientContext context;

    Status status = stub_->GetPIR(&context, request, &reply);

    if (status.ok()) {

      stringstream read_stream;
      read_stream.str(reply.data());
      /////////////////////////////////Client///////////////////////////////////////////
      // Read data from the binary file into the stringstream
      PirReply anwser = pirClient->deserialize_reply(read_stream);

      // Measure response extraction
      auto time_decode_s = high_resolution_clock::now();
      vector<uint8_t> elems = pirClient->decode_reply(anwser, offset);
      auto time_decode_e = high_resolution_clock::now();
      Log.ExtTime = duration_cast<microseconds>(time_decode_e - time_decode_s).count();

      string decodedVal = VectorToHexString(elems);
      cout <<"Server response: "<<decodedVal << endl;
      Log.Msg = "Decode val: " + decodedVal;
      //validate with database
      //std::string result = ValidateResult(jsonDBFileName,elems,decodedVal);
      return "The strings are EQUAL.";
    }
    else {
      Log.Msg = "GetPIRAnsFromServer failed. Please check connection";
      std::cout << status.error_code() << ": " << status.error_message()
      << std::endl;
      return "RPC failed";
    }
  }


  std::string ValidateResult(std::string jsonFile, const vector<uint8_t> &elems, const std::string &decodedVal){
    Document doc;
    uint64_t number_of_items;
    uint64_t size_per_item;

    get_seal_params(jsonFile, number_of_items, size_per_item, doc);
    cout <<"Validate result with database: ";
    assert(elems.size() == size_per_item);
    //validate
    const Value& obj = doc[0];
    Value::ConstMemberIterator it = obj.MemberBegin();
    std::advance(it, ele_index); // Move the iterator to the i-th position
    //string key = it->name.GetString();
    string value = it->value.GetString();
    cout << value << endl;
    int result = decodedVal.compare(value);
    if (result == 0) {
      return "The strings are EQUAL.";
    } else {
      return "The strings are NOT equal.";
    }
  }


  int GenQuery(uint64_t number_of_items, uint64_t size_per_item, PIRClient* &pirClient, RequestData &requestData){

    uint32_t logt = 20;
    uint32_t d = 2;
    bool use_symmetric = true; // use symmetric encryption instead of public key
    // (recommended for smaller query)
    bool use_batching = true;  // pack as many elements as possible into a BFV
    // plaintext (recommended)
    bool use_recursive_mod_switching = true;

    auto ecp = loadFileToString("encryption_parameters.bin");
    if (ecp.size() == 0) {
      return -1;
    }

    EncryptionParameters enc_params = load_encryption_parameters_from_string(ecp);
    // Verifying SEAL parameters
    verify_encryption_params(enc_params);

    PirParams pir_params;
    gen_pir_params(number_of_items, size_per_item, d, enc_params, pir_params, use_symmetric, use_batching, use_recursive_mod_switching);

    pirClient = new PIRClient(enc_params, pir_params);
    // Generating galois keys for client
    GaloisKeys galois_keys = pirClient->generate_galois_keys();

    string gkey = SEALSerialize(galois_keys);

    //Generate query
    uint64_t index = pirClient->get_fv_index(ele_index);   // index of FV plaintext
    offset = pirClient->get_fv_offset(ele_index); // offset in FV plaintext
    cout << "Main: element index = " << ele_index << " from [0, "
    << number_of_items - 1<< "]" << endl;

    // Query generation
    auto time_query_s = high_resolution_clock::now();
    PirQuery query = pirClient->generate_query(index);
    auto time_query_e = high_resolution_clock::now();
    Log.QueryTime = duration_cast<microseconds>(time_query_e - time_query_s).count();

    //Measure serialized query generation (useful for sending over the network)
    stringstream client_stream;
    auto time_s_query_s = high_resolution_clock::now();
    int query_size = pirClient->generate_serialized_query(index, client_stream);
    auto time_s_query_e = high_resolution_clock::now();
    auto time_s_query_us =
    duration_cast<microseconds>(time_s_query_e - time_s_query_s).count();
    Log.QuerySize = query_size;

    requestData.set_clientid(1);
    requestData.set_requestid(1);
    requestData.mutable_pirconfig()->set_use_symmetric(use_symmetric);
    requestData.mutable_pirconfig()->set_use_batching(use_batching);
    requestData.mutable_pirconfig()->set_use_recursive_mod_switching(use_recursive_mod_switching);
    requestData.mutable_pirconfig()->set_d(2);
    requestData.mutable_pirconfig()->set_num_of_items(number_of_items);
    requestData.mutable_pirconfig()->set_size_per_item(size_per_item);
    requestData.mutable_pirconfig()->mutable_epparams()->assign(ecp);
    requestData.set_gkey(gkey);
    requestData.set_query(client_stream.str());
    requestData.set_dbname(this->jsonDBFileName);

    return 0;
  }
  
  int countFirstHostAddr(const std::vector<ClientRequestInfo>& requestInfoVector) {
    if (requestInfoVector.empty()) {
        // Handle the case where the vector is empty
        return 0;
    }

    // Extract the first hostAddr from the first element of the vector
    std::string firstHostAddr = requestInfoVector[0].hostAddr;

    // Count the occurrences of the first hostAddr in the vector
    int count = 0;
    for (const auto& requestInfo : requestInfoVector) {
        if (requestInfo.hostAddr == firstHostAddr) {
            count++;
        }
    }

    return count;
  }

private:
  std::unique_ptr<PIRService::Stub> stub_;
  uint64_t ele_index;
  uint64_t offset;
  std::string jsonDBFileName;
public:
  ClientResultLog Log;
};

int main(int argc, char** argv) {
  // Get list server
  std::vector<ClientRequestInfo> listServers = getListServers("servers_list.txt");
  int i,j = 0;

  // Extract the first hostAddr from the first element of the vector
   std::string firstHostAddr = listServers[0].hostAddr;

  // Count the occurrences of the first hostAddr in the vector
  int occurrences = 0;
  for (const auto& requestInfo : listServers) {
      if (requestInfo.hostAddr == firstHostAddr) {
          occurrences++;
      }
  }

  int total = listServers.size();
  int num_servers = total/occurrences;

  cout<<"num_servers = "<< num_servers <<endl;

  ClientWorker* arrayClient[total];
  pir_message::DBInfo dbInfo[total];

  RequestData requestData[total];
  PIRClient* pirClient[total];

  int resGetDBInfo[num_servers];
  int resGenQuery[num_servers];
  int resPIRAnsFromServer[num_servers];

  // Use futures to store the results of the asynchronous tasks
  vector<future<int>> fGetDBInfo(num_servers);
  vector<future<int>> fGenQuery(num_servers);
  vector<future<int>> fPIRAnsFromServer(num_servers);

  fLogfile.open(CLIENT_LOG_FILE, ios::app);
  vector<ClientRequestInfo>::iterator requestInfo;

  for (requestInfo = listServers.begin(); requestInfo < listServers.end(); requestInfo++) {
      requestInfo->print();
      if (j < total){
          arrayClient[j] = new ClientWorker(grpc::CreateChannel(requestInfo->hostAddr, grpc::InsecureChannelCredentials()), requestInfo->jsDBFile, requestInfo->eIndex);
	      arrayClient[j]->Log.Server = requestInfo->hostAddr;
	      j++;
      }
  }

  for (int k = 0; k < occurrences; k++) {
      cout<<"================ BEGIN ============="<<endl;

      // Function to execute in a thread to get DBInfo
      auto getDBInfoThread = [&](int index) {
          int result = arrayClient[index]->GetDBInfo(dbInfo[index]);
          return result;
      };
   
      // Function to execute in a thread to generate Query
      auto GenQueryThread = [&](int index) {
          if (resGetDBInfo[index] >= 0) {
              int result = arrayClient[index]->GenQuery(dbInfo[index].num_of_items(), dbInfo[index].size_per_item(), pirClient[index], requestData[index]);
              return result;
          }
          return -1; // or some error code indicating failure
      };
   
      // Function to execute in a thread to get PIR from the server
      auto getPIRAnsFromServerThread = [&](int index) {
          if (resGenQuery[index] >= 0) {
              arrayClient[index]->GetPIRAnsFromServer(pirClient[index], requestData[index], num_servers);
              clientLogResult(&fLogfile, &arrayClient[index]->Log);
              return 1;
          }
          return -1;
      };
   
   	  // Get DBInfo
   	  for (i = 0; i < num_servers; i++) {
   	    fGetDBInfo[i] = async(getDBInfoThread, i + k*num_servers);
   	  }
   
   	  // Get results
   	  for (i = 0; i < num_servers; i++) {
   	    resGetDBInfo[i] = fGetDBInfo[i].get();
   	  }
   
   	  // Generate Query
   	  for (i = 0; i < num_servers; i++) {
   	    fGenQuery[i] = async(GenQueryThread, i + k*num_servers);
   	  }
   
   	  // Get results
   	  for (i = 0; i < num_servers; i++) {
   	    resGenQuery[i] = fGenQuery[i].get();
   	  }
   
   	  // Get PIR from the server
   	  for (i = 0; i < num_servers; i++) {
   	    fPIRAnsFromServer[i] = async(getPIRAnsFromServerThread, i + k*num_servers);
   	  }
   
   	  // Wait for all threads to finish
   	  for (i = 0; i < num_servers; i++) {
   	    resPIRAnsFromServer[i] = fPIRAnsFromServer[i].get();
   	  }

	     cout<<"================ END ==============="<< k << endl;
      // Sleep for 2 second
      std::this_thread::sleep_for(std::chrono::seconds(2));
  }
  //free memory
  for (i = 0; i < total; i++)
  {
      delete arrayClient[i];
      delete pirClient[i];
      requestData[i].Clear();
  }

  fLogfile.close();
  listServers.clear();

  return 0;
}

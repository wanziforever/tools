#!/usr/local/bin/thrift --gen cpp  

namespace cpp SACService
namespace java com.hisense.hitv.sacservice.rpc


//query user info
struct out_apiauth
{
    1:i32 resultcode,
    2:i32 subscriberid,      
    3:i32 customerid,
    4:string devid,
    5:i64 appkey,
    6:string loginname
}

//create token
struct in_storetokeninfo
{
	1:i32 customerid,
	2:string devid,
	3:i64 appkey,
	4:string loginname
}

struct in_createtoken
{
    1:i64 subcriber_id,
    2:string session_id,
    3:i64 create_time,
    4:i32 expired_time,
    5:string client_ip
}

struct out_createtoken
{
    1:i32 resultcode,
    2:in_createtoken tokeninfo,
    3:i32 errorcode	
}


service SACService {
    out_apiauth apiAuth(1:string token,2:string apicode,3:string appkey),
    out_createtoken createToken(1:in_createtoken inpara,2:in_storetokeninfo inpara_add),
    out_createtoken getToken(1:in_createtoken inpara),
    out_createtoken deleteToken(1:in_createtoken inpara)
}



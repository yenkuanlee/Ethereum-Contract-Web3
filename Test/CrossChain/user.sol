pragma solidity ^0.4.0;

contract Users {

    struct Person {
	string Ehash;
	string host;
        string passwd;
        string tag;
	string role;
    }

    function Users() public{
    }

    mapping(bytes24 => Person) public user;
    
    function setNode(bytes24 name, string e, string h, string p, string t, string r){
	user[name].Ehash = e;
	user[name].host = h;
	user[name].passwd = p;
	user[name].tag = t;
	user[name].role = r;
    }

    function GetEhash(bytes24 person) constant returns (string) {
        return user[person].Ehash;
    }

    function GetInfo(bytes24 name, string p) public returns (string,string) {
	if(keccak256(user[name].passwd) == keccak256(p)){
	    return (user[name].Ehash,user[name].host);
	}
    }

    function ModifyPasswd(bytes24 name, string op, string np) public returns (string) {
        if(keccak256(user[name].passwd) == keccak256(op)){
	    user[name].passwd = np;
            return "success";
        }
	else{
	    return "wrong op";
	}
    }

}

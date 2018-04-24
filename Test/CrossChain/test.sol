pragma solidity ^0.4.0;

contract test {

    function test() public{
    }


    function GetEhash() constant returns (uint256) {

        return msg.sender.balance;
    }


}

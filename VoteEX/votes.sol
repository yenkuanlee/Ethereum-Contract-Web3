pragma solidity ^0.4.0;
contract Ballot {

   struct Voter {
        uint weight;               //投票權     (0=無授權, 1=已授權)
        uint vote;                //投票給誰
    }
    struct Proposal {
        uint voteCount;            //獲得票數
    }

    uint public NProposals;
    address public chairperson;   
    mapping(address => Voter) public voters;
    Proposal[] public proposals;

    // 建立新的投票
    // _numProposals 候選人數量
    // Create a new ballot with $(_numProposals) different proposals.
    function Ballot(uint _numProposals) public {
	NProposals = _numProposals;
        chairperson = msg.sender;
        voters[chairperson].weight = _numProposals;
        proposals.length = _numProposals;
    }

    // 投票主持人給予他人投票權力
    // toVoter  被授權者帳戶地址
    /// Give $(toVoter) the right to vote on this ballot.
    /// May only be called by $(chairperson).
    function giveRightToVote(address toVoter) public {
        if (msg.sender != chairperson) return;
        voters[toVoter].weight = NProposals;
    }


    // 投票
    // toProposal  要投的候選人編號
    /// Give a single vote to proposal $(toProposal).
    function vote(uint toProposal, uint VC) public {
        Voter storage sender = voters[msg.sender];
        if (toProposal >= proposals.length || VC > sender.weight) return;
        sender.vote = toProposal;
        proposals[toProposal].voteCount += VC;
	sender.weight -= VC;
    }
    
    //計算票選的贏家
    function winningProposal() public constant returns (uint _winningProposal) {
        uint winningVoteCount = 0;
        for (uint prop = 0; prop < proposals.length; prop++)
            if (proposals[prop].voteCount > winningVoteCount) {          //票數超過原winningProposal時, 會更換贏家
                winningVoteCount = proposals[prop].voteCount;
                _winningProposal = prop;
            }
    }

    function GetVoteCount(uint num) public constant returns (uint VC) {
	VC = proposals[num].voteCount;
    }
    
    function GetRemainVoteWeight(address voter) public constant returns (uint RVW) {
	Voter storage sender = voters[voter];
	RVW = sender.weight;
    }
}

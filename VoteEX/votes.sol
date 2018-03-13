pragma solidity ^0.4.0;
contract Ballot {

   struct Voter {
        uint weight;
        uint vote;
    }
    struct Proposal {
        uint voteCount;
    }

    uint public NProposals;
    address public chairperson;   
    mapping(address => Voter) public voters;
    Proposal[] public proposals;

    function Ballot(uint _numProposals) public {
	NProposals = _numProposals;
        chairperson = msg.sender;
        voters[chairperson].weight = _numProposals;
        proposals.length = _numProposals;
    }

    function giveRightToVote(address toVoter) public {
        if (msg.sender != chairperson) return;
        voters[toVoter].weight = NProposals;
    }


    function vote(uint toProposal, uint VC) public {
        Voter storage sender = voters[msg.sender];
        if (toProposal >= proposals.length || VC > sender.weight) return;
        sender.vote = toProposal;
        proposals[toProposal].voteCount += VC;
	sender.weight -= VC;
    }
    
    function winningProposal() public constant returns (uint _winningProposal) {
        uint winningVoteCount = 0;
        for (uint prop = 0; prop < proposals.length; prop++)
            if (proposals[prop].voteCount > winningVoteCount) {
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

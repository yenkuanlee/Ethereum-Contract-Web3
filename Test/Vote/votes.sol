pragma solidity ^0.4.0;
contract Ballot {

   struct Voter {
        uint weight;               //投票權     (0=無授權, 1=已授權)
        bool voted;                //是否已投票 (false=未投, true=已投)
        uint8 vote;                //投票給誰
        address delegate;          //代投人帳戶地址
    }
    struct Proposal {
        uint voteCount;            //獲得票數
    }

    address public chairperson;   
    mapping(address => Voter) public voters;
    Proposal[] public proposals;

    // 建立新的投票
    // _numProposals 候選人數量
    // Create a new ballot with $(_numProposals) different proposals.
    function Ballot(uint8 _numProposals) public {
        chairperson = msg.sender;
        voters[chairperson].weight = 1;
        proposals.length = _numProposals;
    }

    // 投票主持人給予他人投票權力
    // toVoter  被授權者帳戶地址
    /// Give $(toVoter) the right to vote on this ballot.
    /// May only be called by $(chairperson).
    function giveRightToVote(address toVoter) public {
        if (msg.sender != chairperson || voters[toVoter].voted) return;
        voters[toVoter].weight = 1;                                      //被授權者的權力值改為1
    }

    // 設定代投者
    // to  被指定代投的帳戶地址
    /// Delegate your vote to the voter $(to).
    function delegate(address to) public {
        Voter storage sender = voters[msg.sender]; // assigns reference
        if (sender.voted) return;
        while (voters[to].delegate != address(0) && voters[to].delegate != msg.sender)
            to = voters[to].delegate;
        if (to == msg.sender) return;
        sender.voted = true;
        sender.delegate = to;                                           //紀錄代投者資訊
        Voter storage delegateTo = voters[to];                        
        if (delegateTo.voted)                                           //賦予(轉換)權力
            proposals[delegateTo.vote].voteCount += sender.weight;
        else
            delegateTo.weight += sender.weight;
    }

    // 投票
    // toProposal  要投的候選人編號
    /// Give a single vote to proposal $(toProposal).
    function vote(uint8 toProposal) public {
        Voter storage sender = voters[msg.sender];
        if (sender.voted || toProposal >= proposals.length) return;
        sender.voted = true;
        sender.vote = toProposal;
        proposals[toProposal].voteCount += sender.weight;                //將投票的對象票數+1
    }
    
    //計算票選的贏家
    function winningProposal() public constant returns (uint8 _winningProposal) {
        uint256 winningVoteCount = 0;
        for (uint8 prop = 0; prop < proposals.length; prop++)
            if (proposals[prop].voteCount > winningVoteCount) {          //票數超過原winningProposal時, 會更換贏家
                winningVoteCount = proposals[prop].voteCount;
                _winningProposal = prop;
            }
    }
}
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IExternalOracle
 * @notice Interface for external oracle interactions
 * @dev Provides capability validation and attestation verification
 */
interface IExternalOracle {
    /**
     * @notice Gets the ARM (Attestation Reliability Metric) score for a user
     * @param user The address to check
     * @return armScore The ARM score scaled by 1000 (e.g., 902 = 0.902)
     */
    function getARMScore(address user) external view returns (uint256 armScore);

    /**
     * @notice Gets the ES (Ethical Score) for a user
     * @param user The address to check
     * @return esScore The ethical score (0-100)
     */
    function getESScore(address user) external view returns (uint256 esScore);

    /**
     * @notice Verifies triad attestation from the oracle
     * @param attestationHash The hash of the attestation data
     * @return isValid Whether the attestation is valid
     */
    function verifyTriadAttestation(bytes32 attestationHash) external view returns (bool isValid);
}

/**
 * @title ScenarioSelector
 * @notice Dual governance mechanism with triad attestation system and saturation veil
 * @dev Implements EIP-712 typed data structures for proposal and execution validation
 */
contract ScenarioSelector {
    // ============ Constants ============
    
    /// @notice Minimum ARM threshold for qualification (0.902 * 1000 = 902)
    uint256 public constant ARM_THRESHOLD = 902;
    
    /// @notice Minimum ES threshold for qualification
    uint256 public constant ES_THRESHOLD = 50;
    
    /// @notice Maximum saturation level before veil activation
    uint256 public constant SATURATION_VEIL_THRESHOLD = 1000;
    
    /// @notice EIP-712 domain separator typehash
    bytes32 public constant DOMAIN_TYPEHASH = keccak256(
        "EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"
    );
    
    /// @notice EIP-712 proposal typehash
    bytes32 public constant PROPOSAL_TYPEHASH = keccak256(
        "Proposal(uint256 proposalId,address proposer,bytes32 scenarioHash,uint256 deadline,uint256 nonce)"
    );
    
    /// @notice EIP-712 execution typehash
    bytes32 public constant EXECUTION_TYPEHASH = keccak256(
        "Execution(uint256 proposalId,address executor,bytes32 attestationHash,uint256 timestamp)"
    );
    
    // ============ State Variables ============
    
    /// @notice External oracle for capability validation
    IExternalOracle public oracle;
    
    /// @notice Domain separator for EIP-712
    bytes32 public immutable DOMAIN_SEPARATOR;
    
    /// @notice Current saturation level
    uint256 public saturationLevel;
    
    /// @notice Whether the saturation veil is active
    bool public veilActive;
    
    /// @notice Counter for proposal IDs
    uint256 public proposalCount;
    
    /// @notice Mapping of user nonces for EIP-712 signatures
    mapping(address => uint256) public nonces;
    
    /// @notice Mapping of proposals
    mapping(uint256 => Proposal) public proposals;
    
    /// @notice Mapping of triad attestations
    mapping(uint256 => TriadAttestation) public attestations;
    
    // ============ Structs ============
    
    /// @notice Governance scenario states
    enum ScenarioState {
        Pending,
        Attested,
        Approved,
        Executed,
        Rejected,
        Veiled
    }
    
    /// @notice Proposal data structure
    struct Proposal {
        uint256 id;
        address proposer;
        bytes32 scenarioHash;
        uint256 deadline;
        ScenarioState state;
        uint256 createdAt;
        uint256 attestationCount;
    }
    
    /// @notice Triad attestation data structure
    struct TriadAttestation {
        address[3] attestors;
        bytes32[3] attestationHashes;
        uint256 completedAt;
        bool isComplete;
    }
    
    // ============ Events ============
    
    /// @notice Emitted when a proposal is created
    event ProposalCreated(
        uint256 indexed proposalId,
        address indexed proposer,
        bytes32 scenarioHash,
        uint256 deadline,
        ScenarioState state
    );
    
    /// @notice Emitted when a state transition occurs
    event StateTransition(
        uint256 indexed proposalId,
        ScenarioState indexed fromState,
        ScenarioState indexed toState,
        string transitionCause
    );
    
    /// @notice Emitted when an attestation is added
    event AttestationAdded(
        uint256 indexed proposalId,
        address indexed attestor,
        bytes32 attestationHash,
        uint256 attestationIndex
    );
    
    /// @notice Emitted when triad attestation is complete
    event TriadAttestationComplete(
        uint256 indexed proposalId,
        address[3] attestors
    );
    
    /// @notice Emitted when saturation veil is activated
    event SaturationVeilActivated(
        uint256 saturationLevel,
        uint256 timestamp
    );
    
    /// @notice Emitted when saturation veil is deactivated
    event SaturationVeilDeactivated(
        uint256 previousLevel,
        uint256 timestamp
    );
    
    /// @notice Emitted when proposal is executed
    event ProposalExecuted(
        uint256 indexed proposalId,
        address indexed executor,
        bytes32 attestationHash,
        uint256 timestamp
    );
    
    /// @notice Emitted when qualification status changes
    event QualificationStatusChanged(
        address indexed user,
        bool isQualified,
        uint256 armScore,
        uint256 esScore
    );
    
    // ============ Errors ============
    
    error UnqualifiedProposer(address proposer, uint256 armScore, uint256 esScore);
    error InvalidSignature();
    error ProposalExpired(uint256 proposalId, uint256 deadline);
    error InvalidProposalState(uint256 proposalId, ScenarioState currentState, ScenarioState expectedState);
    error VeilActive();
    error TriadIncomplete(uint256 proposalId, uint256 currentCount);
    error AlreadyAttested(uint256 proposalId, address attestor);
    error OracleVerificationFailed(bytes32 attestationHash);
    
    // ============ Constructor ============
    
    /**
     * @notice Initializes the ScenarioSelector contract
     * @param _oracle Address of the external oracle
     */
    constructor(address _oracle) {
        oracle = IExternalOracle(_oracle);
        
        DOMAIN_SEPARATOR = keccak256(
            abi.encode(
                DOMAIN_TYPEHASH,
                keccak256(bytes("ScenarioSelector")),
                keccak256(bytes("1")),
                block.chainid,
                address(this)
            )
        );
    }
    
    // ============ External Functions ============
    
    /**
     * @notice Checks if an address is qualified based on ES/ARM scores
     * @param user The address to check
     * @return qualified Whether the user meets ARM ≥ 0.902 threshold
     * @return armScore The user's ARM score
     * @return esScore The user's ES score
     */
    function isQualified(address user) external view returns (
        bool qualified,
        uint256 armScore,
        uint256 esScore
    ) {
        armScore = oracle.getARMScore(user);
        esScore = oracle.getESScore(user);
        qualified = armScore >= ARM_THRESHOLD && esScore >= ES_THRESHOLD;
    }
    
    /**
     * @notice Creates a new governance proposal
     * @param scenarioHash Hash of the scenario data
     * @param deadline Proposal expiration timestamp
     * @param v ECDSA signature parameter
     * @param r ECDSA signature parameter
     * @param s ECDSA signature parameter
     * @return proposalId The ID of the created proposal
     */
    function createProposal(
        bytes32 scenarioHash,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external returns (uint256 proposalId) {
        if (veilActive) revert VeilActive();
        
        // Verify qualification
        uint256 armScore = oracle.getARMScore(msg.sender);
        uint256 esScore = oracle.getESScore(msg.sender);
        
        if (armScore < ARM_THRESHOLD || esScore < ES_THRESHOLD) {
            revert UnqualifiedProposer(msg.sender, armScore, esScore);
        }
        
        // Verify EIP-712 signature
        uint256 nonce = nonces[msg.sender];
        bytes32 structHash = keccak256(
            abi.encode(
                PROPOSAL_TYPEHASH,
                proposalCount,
                msg.sender,
                scenarioHash,
                deadline,
                nonce
            )
        );
        bytes32 digest = keccak256(
            abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash)
        );
        
        address signer = ecrecover(digest, v, r, s);
        if (signer != msg.sender) revert InvalidSignature();
        
        // Increment nonce
        nonces[msg.sender] = nonce + 1;
        
        // Create proposal
        proposalId = proposalCount++;
        proposals[proposalId] = Proposal({
            id: proposalId,
            proposer: msg.sender,
            scenarioHash: scenarioHash,
            deadline: deadline,
            state: ScenarioState.Pending,
            createdAt: block.timestamp,
            attestationCount: 0
        });
        
        // Update saturation
        _updateSaturation(1);
        
        emit ProposalCreated(proposalId, msg.sender, scenarioHash, deadline, ScenarioState.Pending);
        emit QualificationStatusChanged(msg.sender, true, armScore, esScore);
    }
    
    /**
     * @notice Adds an attestation to a proposal (requires 3 for completion)
     * @param proposalId The proposal to attest to
     * @param attestationHash Hash of the attestation data
     */
    function addAttestation(uint256 proposalId, bytes32 attestationHash) external {
        Proposal storage proposal = proposals[proposalId];
        
        if (proposal.state != ScenarioState.Pending) {
            revert InvalidProposalState(proposalId, proposal.state, ScenarioState.Pending);
        }
        
        if (block.timestamp > proposal.deadline) {
            revert ProposalExpired(proposalId, proposal.deadline);
        }
        
        // Verify attestor qualification
        uint256 armScore = oracle.getARMScore(msg.sender);
        uint256 esScore = oracle.getESScore(msg.sender);
        
        if (armScore < ARM_THRESHOLD || esScore < ES_THRESHOLD) {
            revert UnqualifiedProposer(msg.sender, armScore, esScore);
        }
        
        // Verify attestation with oracle
        if (!oracle.verifyTriadAttestation(attestationHash)) {
            revert OracleVerificationFailed(attestationHash);
        }
        
        // Check if already attested
        TriadAttestation storage triad = attestations[proposalId];
        for (uint256 i = 0; i < 3; i++) {
            if (triad.attestors[i] == msg.sender) {
                revert AlreadyAttested(proposalId, msg.sender);
            }
        }
        
        // Add attestation
        uint256 index = proposal.attestationCount;
        triad.attestors[index] = msg.sender;
        triad.attestationHashes[index] = attestationHash;
        proposal.attestationCount++;
        
        emit AttestationAdded(proposalId, msg.sender, attestationHash, index);
        
        // Check if triad is complete
        if (proposal.attestationCount == 3) {
            triad.completedAt = block.timestamp;
            triad.isComplete = true;
            
            ScenarioState previousState = proposal.state;
            proposal.state = ScenarioState.Attested;
            
            emit TriadAttestationComplete(proposalId, triad.attestors);
            emit StateTransition(proposalId, previousState, ScenarioState.Attested, "Triad attestation complete");
        }
    }
    
    /**
     * @notice Executes an attested proposal
     * @param proposalId The proposal to execute
     * @param v ECDSA signature parameter
     * @param r ECDSA signature parameter
     * @param s ECDSA signature parameter
     */
    function executeProposal(
        uint256 proposalId,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external {
        if (veilActive) revert VeilActive();
        
        Proposal storage proposal = proposals[proposalId];
        
        if (proposal.state != ScenarioState.Attested) {
            revert InvalidProposalState(proposalId, proposal.state, ScenarioState.Attested);
        }
        
        if (block.timestamp > proposal.deadline) {
            revert ProposalExpired(proposalId, proposal.deadline);
        }
        
        // Verify executor qualification
        uint256 armScore = oracle.getARMScore(msg.sender);
        uint256 esScore = oracle.getESScore(msg.sender);
        
        if (armScore < ARM_THRESHOLD || esScore < ES_THRESHOLD) {
            revert UnqualifiedProposer(msg.sender, armScore, esScore);
        }
        
        // Verify EIP-712 execution signature
        TriadAttestation storage triad = attestations[proposalId];
        bytes32 combinedHash = keccak256(
            abi.encodePacked(
                triad.attestationHashes[0],
                triad.attestationHashes[1],
                triad.attestationHashes[2]
            )
        );
        
        bytes32 structHash = keccak256(
            abi.encode(
                EXECUTION_TYPEHASH,
                proposalId,
                msg.sender,
                combinedHash,
                block.timestamp
            )
        );
        bytes32 digest = keccak256(
            abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash)
        );
        
        address signer = ecrecover(digest, v, r, s);
        if (signer != msg.sender) revert InvalidSignature();
        
        // Execute
        ScenarioState previousState = proposal.state;
        proposal.state = ScenarioState.Executed;
        
        // Decrease saturation on successful execution
        _updateSaturation(-1);
        
        emit ProposalExecuted(proposalId, msg.sender, combinedHash, block.timestamp);
        emit StateTransition(proposalId, previousState, ScenarioState.Executed, "Execution validated");
    }
    
    /**
     * @notice Gets the current saturation level and veil status
     * @return level Current saturation level
     * @return isVeilActive Whether the saturation veil is active
     */
    function getSaturationStatus() external view returns (uint256 level, bool isVeilActive) {
        return (saturationLevel, veilActive);
    }
    
    /**
     * @notice Gets proposal details
     * @param proposalId The proposal ID
     * @return proposal The proposal data
     */
    function getProposal(uint256 proposalId) external view returns (Proposal memory) {
        return proposals[proposalId];
    }
    
    /**
     * @notice Gets triad attestation details
     * @param proposalId The proposal ID
     * @return attestation The triad attestation data
     */
    function getTriadAttestation(uint256 proposalId) external view returns (TriadAttestation memory) {
        return attestations[proposalId];
    }
    
    /**
     * @notice Manually deactivates the saturation veil (admin function)
     * @dev In production, this would have access control
     */
    function deactivateVeil() external {
        uint256 previousLevel = saturationLevel;
        saturationLevel = 0;
        veilActive = false;
        
        emit SaturationVeilDeactivated(previousLevel, block.timestamp);
    }
    
    // ============ Internal Functions ============
    
    /**
     * @notice Updates saturation level and manages veil activation
     * @param delta Change in saturation (positive or negative)
     */
    function _updateSaturation(int256 delta) internal {
        if (delta > 0) {
            saturationLevel += uint256(delta);
        } else if (delta < 0 && saturationLevel > 0) {
            uint256 absValue = uint256(-delta);
            if (saturationLevel >= absValue) {
                saturationLevel -= absValue;
            } else {
                saturationLevel = 0;
            }
        }
        
        // Check veil activation
        if (saturationLevel >= SATURATION_VEIL_THRESHOLD && !veilActive) {
            veilActive = true;
            emit SaturationVeilActivated(saturationLevel, block.timestamp);
        } else if (saturationLevel < SATURATION_VEIL_THRESHOLD && veilActive) {
            veilActive = false;
            emit SaturationVeilDeactivated(saturationLevel, block.timestamp);
        }
    }
}

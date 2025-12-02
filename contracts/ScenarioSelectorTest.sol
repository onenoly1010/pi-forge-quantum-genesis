// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ScenarioSelector.sol";

/**
 * @title MockExternalOracle
 * @notice Mock oracle for testing ScenarioSelector
 */
contract MockExternalOracle is IExternalOracle {
    mapping(address => uint256) public armScores;
    mapping(address => uint256) public esScores;
    mapping(bytes32 => bool) public validAttestations;
    
    function setARMScore(address user, uint256 score) external {
        armScores[user] = score;
    }
    
    function setESScore(address user, uint256 score) external {
        esScores[user] = score;
    }
    
    function setAttestationValid(bytes32 attestationHash, bool valid) external {
        validAttestations[attestationHash] = valid;
    }
    
    function getARMScore(address user) external view override returns (uint256) {
        return armScores[user];
    }
    
    function getESScore(address user) external view override returns (uint256) {
        return esScores[user];
    }
    
    function verifyTriadAttestation(bytes32 attestationHash) external view override returns (bool) {
        return validAttestations[attestationHash];
    }
}

/**
 * @title ScenarioSelectorTest
 * @notice Test contract for ScenarioSelector
 * @dev Contains test scenarios for dual governance and triad attestation
 */
contract ScenarioSelectorTest {
    ScenarioSelector public scenarioSelector;
    MockExternalOracle public mockOracle;
    
    // Test accounts
    address public constant QUALIFIED_USER_1 = address(0x1111111111111111111111111111111111111111);
    address public constant QUALIFIED_USER_2 = address(0x2222222222222222222222222222222222222222);
    address public constant QUALIFIED_USER_3 = address(0x3333333333333333333333333333333333333333);
    address public constant UNQUALIFIED_USER = address(0x4444444444444444444444444444444444444444);
    
    // Test data
    bytes32 public constant TEST_SCENARIO_HASH = keccak256("test_scenario_v1");
    bytes32 public constant TEST_ATTESTATION_1 = keccak256("attestation_1");
    bytes32 public constant TEST_ATTESTATION_2 = keccak256("attestation_2");
    bytes32 public constant TEST_ATTESTATION_3 = keccak256("attestation_3");
    
    // Events for test results
    event TestResult(string testName, bool passed, string message);
    
    /**
     * @notice Deploys and initializes test infrastructure
     */
    constructor() {
        // Deploy mock oracle
        mockOracle = new MockExternalOracle();
        
        // Deploy ScenarioSelector with mock oracle
        scenarioSelector = new ScenarioSelector(address(mockOracle));
        
        // Setup qualified users (ARM >= 0.902, ES >= 50)
        mockOracle.setARMScore(QUALIFIED_USER_1, 950); // 0.950
        mockOracle.setESScore(QUALIFIED_USER_1, 75);
        
        mockOracle.setARMScore(QUALIFIED_USER_2, 920); // 0.920
        mockOracle.setESScore(QUALIFIED_USER_2, 60);
        
        mockOracle.setARMScore(QUALIFIED_USER_3, 902); // 0.902 (exactly at threshold)
        mockOracle.setESScore(QUALIFIED_USER_3, 50);
        
        // Setup unqualified user (ARM < 0.902)
        mockOracle.setARMScore(UNQUALIFIED_USER, 800); // 0.800 (below threshold)
        mockOracle.setESScore(UNQUALIFIED_USER, 90);
        
        // Setup valid attestations
        mockOracle.setAttestationValid(TEST_ATTESTATION_1, true);
        mockOracle.setAttestationValid(TEST_ATTESTATION_2, true);
        mockOracle.setAttestationValid(TEST_ATTESTATION_3, true);
    }
    
    /**
     * @notice Tests isQualified function with qualified user
     */
    function testIsQualifiedWithQualifiedUser() external {
        (bool qualified, uint256 armScore, uint256 esScore) = scenarioSelector.isQualified(QUALIFIED_USER_1);
        
        bool passed = qualified && armScore == 950 && esScore == 75;
        emit TestResult(
            "testIsQualifiedWithQualifiedUser",
            passed,
            passed ? "Qualified user correctly identified" : "Failed to identify qualified user"
        );
    }
    
    /**
     * @notice Tests isQualified function with unqualified user
     */
    function testIsQualifiedWithUnqualifiedUser() external {
        (bool qualified, uint256 armScore, uint256 esScore) = scenarioSelector.isQualified(UNQUALIFIED_USER);
        
        bool passed = !qualified && armScore == 800 && esScore == 90;
        emit TestResult(
            "testIsQualifiedWithUnqualifiedUser",
            passed,
            passed ? "Unqualified user correctly identified" : "Failed to identify unqualified user"
        );
    }
    
    /**
     * @notice Tests ARM threshold boundary (exactly 0.902)
     */
    function testARMThresholdBoundary() external {
        (bool qualified, uint256 armScore, ) = scenarioSelector.isQualified(QUALIFIED_USER_3);
        
        bool passed = qualified && armScore == 902;
        emit TestResult(
            "testARMThresholdBoundary",
            passed,
            passed ? "ARM threshold boundary correctly handled" : "ARM threshold boundary failed"
        );
    }
    
    /**
     * @notice Tests saturation veil status
     */
    function testSaturationStatus() external {
        (uint256 level, bool isVeilActive) = scenarioSelector.getSaturationStatus();
        
        bool passed = level == 0 && !isVeilActive;
        emit TestResult(
            "testSaturationStatus",
            passed,
            passed ? "Initial saturation status correct" : "Initial saturation status incorrect"
        );
    }
    
    /**
     * @notice Tests EIP-712 domain separator existence
     */
    function testDomainSeparator() external {
        bytes32 domainSeparator = scenarioSelector.DOMAIN_SEPARATOR();
        
        bool passed = domainSeparator != bytes32(0);
        emit TestResult(
            "testDomainSeparator",
            passed,
            passed ? "EIP-712 domain separator configured" : "EIP-712 domain separator missing"
        );
    }
    
    /**
     * @notice Tests proposal count initialization
     */
    function testProposalCountInitialization() external {
        uint256 count = scenarioSelector.proposalCount();
        
        bool passed = count == 0;
        emit TestResult(
            "testProposalCountInitialization",
            passed,
            passed ? "Proposal count initialized to 0" : "Proposal count not initialized correctly"
        );
    }
    
    /**
     * @notice Tests oracle integration
     */
    function testOracleIntegration() external {
        address oracleAddr = address(scenarioSelector.oracle());
        
        bool passed = oracleAddr == address(mockOracle);
        emit TestResult(
            "testOracleIntegration",
            passed,
            passed ? "Oracle correctly integrated" : "Oracle integration failed"
        );
    }
    
    /**
     * @notice Tests constant values
     */
    function testConstants() external {
        bool armThresholdCorrect = scenarioSelector.ARM_THRESHOLD() == 902;
        bool esThresholdCorrect = scenarioSelector.ES_THRESHOLD() == 50;
        bool saturationThresholdCorrect = scenarioSelector.SATURATION_VEIL_THRESHOLD() == 1000;
        
        bool passed = armThresholdCorrect && esThresholdCorrect && saturationThresholdCorrect;
        emit TestResult(
            "testConstants",
            passed,
            passed ? "All constants correctly set" : "Constants not correctly set"
        );
    }
    
    /**
     * @notice Runs all tests
     */
    function runAllTests() external {
        this.testIsQualifiedWithQualifiedUser();
        this.testIsQualifiedWithUnqualifiedUser();
        this.testARMThresholdBoundary();
        this.testSaturationStatus();
        this.testDomainSeparator();
        this.testProposalCountInitialization();
        this.testOracleIntegration();
        this.testConstants();
    }
}

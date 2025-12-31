const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("UniswapV2Router02Slim", function () {
  let factory;
  let router;
  let weth;
  let tokenA;
  let tokenB;
  let pair;
  let owner;
  let user;
  let initCodeHash;

  const TOTAL_SUPPLY = ethers.parseEther("10000");
  const LIQUIDITY_AMOUNT = ethers.parseEther("100");

  beforeEach(async function () {
    [owner, user] = await ethers.getSigners();

    // Deploy mock WETH
    const WETH = await ethers.getContractFactory("MockERC20");
    weth = await WETH.deploy("Wrapped ETH", "WETH", TOTAL_SUPPLY);
    await weth.waitForDeployment();

    // Deploy Factory
    const Factory = await ethers.getContractFactory("UniswapV2Factory");
    factory = await Factory.deploy(owner.address);
    await factory.waitForDeployment();

    // Calculate init code hash
    const Pair = await ethers.getContractFactory("UniswapV2Pair");
    initCodeHash = ethers.keccak256(Pair.bytecode);

    // Deploy Slim Router
    const Router = await ethers.getContractFactory("UniswapV2Router02Slim");
    router = await Router.deploy(
      await factory.getAddress(),
      await weth.getAddress(),
      initCodeHash
    );
    await router.waitForDeployment();

    // Deploy test tokens
    const Token = await ethers.getContractFactory("MockERC20");
    tokenA = await Token.deploy("Token A", "TKA", TOTAL_SUPPLY);
    tokenB = await Token.deploy("Token B", "TKB", TOTAL_SUPPLY);
    await tokenA.waitForDeployment();
    await tokenB.waitForDeployment();

    // Transfer tokens to user
    await tokenA.transfer(user.address, ethers.parseEther("1000"));
    await tokenB.transfer(user.address, ethers.parseEther("1000"));
  });

  describe("Deployment", function () {
    it("Should deploy with correct parameters", async function () {
      expect(await router.factory()).to.equal(await factory.getAddress());
      expect(await router.WETH()).to.equal(await weth.getAddress());
      expect(await router.initCodeHash()).to.equal(initCodeHash);
    });

    it("Should have bytecode size under 24KB", async function () {
      const routerAddress = await router.getAddress();
      const code = await ethers.provider.getCode(routerAddress);
      const bytecodeSize = (code.length - 2) / 2; // Remove 0x and convert to bytes
      
      console.log(`      📏 Bytecode size: ${bytecodeSize} bytes`);
      console.log(`      📊 Percentage of limit: ${((bytecodeSize / 24576) * 100).toFixed(2)}%`);
      
      expect(bytecodeSize).to.be.lessThan(24576, "Bytecode exceeds 24KB limit");
    });
  });

  describe("Add Liquidity", function () {
    it("Should add liquidity to a new pair", async function () {
      const amountA = ethers.parseEther("10");
      const amountB = ethers.parseEther("20");
      const deadline = Math.floor(Date.now() / 1000) + 3600;

      // Approve tokens
      await tokenA.approve(await router.getAddress(), amountA);
      await tokenB.approve(await router.getAddress(), amountB);

      // Add liquidity
      await expect(
        router.addLiquidity(
          await tokenA.getAddress(),
          await tokenB.getAddress(),
          amountA,
          amountB,
          0,
          0,
          owner.address,
          deadline
        )
      ).to.emit(factory, "PairCreated");

      // Verify pair was created
      const pairAddress = await factory.getPair(
        await tokenA.getAddress(),
        await tokenB.getAddress()
      );
      expect(pairAddress).to.not.equal(ethers.ZeroAddress);

      // Verify liquidity was minted
      const Pair = await ethers.getContractFactory("UniswapV2Pair");
      pair = Pair.attach(pairAddress);
      const balance = await pair.balanceOf(owner.address);
      expect(balance).to.be.gt(0);
    });

    it("Should add liquidity to existing pair with correct ratio", async function () {
      const amountA1 = ethers.parseEther("10");
      const amountB1 = ethers.parseEther("20");
      const deadline = Math.floor(Date.now() / 1000) + 3600;

      // First liquidity addition
      await tokenA.approve(await router.getAddress(), amountA1);
      await tokenB.approve(await router.getAddress(), amountB1);
      await router.addLiquidity(
        await tokenA.getAddress(),
        await tokenB.getAddress(),
        amountA1,
        amountB1,
        0,
        0,
        owner.address,
        deadline
      );

      // Second liquidity addition with user
      const amountA2 = ethers.parseEther("5");
      const amountB2 = ethers.parseEther("10");
      
      await tokenA.connect(user).approve(await router.getAddress(), amountA2);
      await tokenB.connect(user).approve(await router.getAddress(), amountB2);
      
      await router.connect(user).addLiquidity(
        await tokenA.getAddress(),
        await tokenB.getAddress(),
        amountA2,
        amountB2,
        0,
        0,
        user.address,
        deadline
      );

      const pairAddress = await factory.getPair(
        await tokenA.getAddress(),
        await tokenB.getAddress()
      );
      const Pair = await ethers.getContractFactory("UniswapV2Pair");
      pair = Pair.attach(pairAddress);
      
      const userBalance = await pair.balanceOf(user.address);
      expect(userBalance).to.be.gt(0);
    });

    it("Should revert if deadline has passed", async function () {
      const amountA = ethers.parseEther("10");
      const amountB = ethers.parseEther("20");
      const pastDeadline = Math.floor(Date.now() / 1000) - 3600;

      await tokenA.approve(await router.getAddress(), amountA);
      await tokenB.approve(await router.getAddress(), amountB);

      await expect(
        router.addLiquidity(
          await tokenA.getAddress(),
          await tokenB.getAddress(),
          amountA,
          amountB,
          0,
          0,
          owner.address,
          pastDeadline
        )
      ).to.be.revertedWithCustomError(router, "Expired");
    });
  });

  describe("Remove Liquidity", function () {
    beforeEach(async function () {
      // Setup: Add initial liquidity
      const amountA = ethers.parseEther("10");
      const amountB = ethers.parseEther("20");
      const deadline = Math.floor(Date.now() / 1000) + 3600;

      await tokenA.approve(await router.getAddress(), amountA);
      await tokenB.approve(await router.getAddress(), amountB);
      
      await router.addLiquidity(
        await tokenA.getAddress(),
        await tokenB.getAddress(),
        amountA,
        amountB,
        0,
        0,
        owner.address,
        deadline
      );

      const pairAddress = await factory.getPair(
        await tokenA.getAddress(),
        await tokenB.getAddress()
      );
      const Pair = await ethers.getContractFactory("UniswapV2Pair");
      pair = Pair.attach(pairAddress);
    });

    it("Should remove liquidity successfully", async function () {
      const liquidity = await pair.balanceOf(owner.address);
      const deadline = Math.floor(Date.now() / 1000) + 3600;

      await pair.approve(await router.getAddress(), liquidity);

      const balanceABefore = await tokenA.balanceOf(owner.address);
      const balanceBBefore = await tokenB.balanceOf(owner.address);

      await router.removeLiquidity(
        await tokenA.getAddress(),
        await tokenB.getAddress(),
        liquidity,
        0,
        0,
        owner.address,
        deadline
      );

      const balanceAAfter = await tokenA.balanceOf(owner.address);
      const balanceBAfter = await tokenB.balanceOf(owner.address);

      expect(balanceAAfter).to.be.gt(balanceABefore);
      expect(balanceBAfter).to.be.gt(balanceBBefore);
    });
  });

  describe("Swaps", function () {
    beforeEach(async function () {
      // Setup: Add liquidity for swaps
      const amountA = ethers.parseEther("100");
      const amountB = ethers.parseEther("200");
      const deadline = Math.floor(Date.now() / 1000) + 3600;

      await tokenA.approve(await router.getAddress(), amountA);
      await tokenB.approve(await router.getAddress(), amountB);
      
      await router.addLiquidity(
        await tokenA.getAddress(),
        await tokenB.getAddress(),
        amountA,
        amountB,
        0,
        0,
        owner.address,
        deadline
      );
    });

    it("Should swap exact tokens for tokens", async function () {
      const amountIn = ethers.parseEther("1");
      const deadline = Math.floor(Date.now() / 1000) + 3600;

      await tokenA.connect(user).approve(await router.getAddress(), amountIn);

      const balanceBBefore = await tokenB.balanceOf(user.address);

      await router.connect(user).swapExactTokensForTokens(
        amountIn,
        0,
        [await tokenA.getAddress(), await tokenB.getAddress()],
        user.address,
        deadline
      );

      const balanceBAfter = await tokenB.balanceOf(user.address);
      expect(balanceBAfter).to.be.gt(balanceBBefore);
    });

    it("Should swap tokens for exact tokens", async function () {
      const amountOut = ethers.parseEther("1");
      const amountInMax = ethers.parseEther("10");
      const deadline = Math.floor(Date.now() / 1000) + 3600;

      await tokenA.connect(user).approve(await router.getAddress(), amountInMax);

      const balanceABefore = await tokenA.balanceOf(user.address);
      const balanceBBefore = await tokenB.balanceOf(user.address);

      await router.connect(user).swapTokensForExactTokens(
        amountOut,
        amountInMax,
        [await tokenA.getAddress(), await tokenB.getAddress()],
        user.address,
        deadline
      );

      const balanceAAfter = await tokenA.balanceOf(user.address);
      const balanceBAfter = await tokenB.balanceOf(user.address);

      expect(balanceAAfter).to.be.lt(balanceABefore);
      expect(balanceBAfter).to.equal(balanceBBefore + amountOut);
    });

    it("Should revert on insufficient output amount", async function () {
      const amountIn = ethers.parseEther("0.01");
      const amountOutMin = ethers.parseEther("100"); // Too high
      const deadline = Math.floor(Date.now() / 1000) + 3600;

      await tokenA.connect(user).approve(await router.getAddress(), amountIn);

      await expect(
        router.connect(user).swapExactTokensForTokens(
          amountIn,
          amountOutMin,
          [await tokenA.getAddress(), await tokenB.getAddress()],
          user.address,
          deadline
        )
      ).to.be.revertedWithCustomError(router, "InsufficientOutputAmount");
    });
  });
});

## Liquidity is a problem; *vaults solves this*

*Max Holloway | November 19, 2024*

The dYdX Chain is uniquely positioned via its permissionless listings product to become the venue for a market on anything. While dYdX Trading has developed the tech to make this vision possible, these markets need *liquidity* for dYdX Chain to become the place where people trade perps on everything. Unfortunately, liquidity is not free.

Liquidity provision typically involves a market-making firm that deploys capital, allocates developer/researcher/trader resources, and warehouses risk with their open positions. For all products -- crypto or otherwise -- liquidity providers are paid in one way or another for the service they provide to the marketplace. This cost generally increases with the amount of resources and risk that the market maker must deploy. Unsurprisingly, these costs are high for crypto market makers, especially for the few brave market makers who are willing to quote bespoke markets -- e.g., election prediction markets -- for which the risk and price discovery mechanism are entirely different.

This inconvenience was observable in the price tag charge for market making services -- \$2,500 per name per month -- which the dYdX Ecosystem Development sponsored a few months ago. In truth, this price tag was likely appropriate for the task at hand -- a firm needed to build out entirely custom infrastructure, they use their own capital to quote, and they had to warehouse risk for the names they were quoting. Market making sucks, and they were paid a high price tag for doing a job that sucks. Fair enough. But if we wanted to scale this out to hundreds of markets, this price tag would quickly approach the millions per year in cost.

Fortunately, if you have a good idea of the fair value of a financial product, the rest of the market making problem is largely mechanical. Knowing this, the dYdX Trading Inc team developed single-name vaults: a vault that allows permissionless deposits, computes a fair price based off of the validator's index price and its own inventory, then quotes multiple bids and offers around that fair price. Given that it is enshrined into the protocol, a single-name vault will have 100% uptime, assuming the chain is running and that there is sufficient capital in the vault. A world with single-name vaults is a world with constant on-chain liquidity. Furthermore, these vaults don't require paying any external market making service providers, and they simply require that anyone deposit USDC in order to run. The promise of single-name vaults was to create a cost-efficient and democratically accessible liquidity provision mechanism on the chain.

I was engaged by the dYdX Ecosystem Development Program to oversee an experimentation period for these vaults. I worked closely with the folks who developed the vaults to selectively deploy capital to vaults to get a better understanding of how they perform, and whether they would work well enough to be a viable solution for the ecosystem to use as a liquidity cornerstone as it grows over the coming years. The answer -- from essentially day one of running the vaults -- is a resounding *yes, vaults will provide immense value to the protocol*.



## Single-name vaults architecture

Single-name vaults are designed as automated liquidity engines embedded directly within the dYdX Chain. The architecture enables each vault to function autonomously, leveraging on-chain data to continuously update quotes and manage risk for the specific perp product that it supports. Here’s how it works in detail:

**Permissionless Deposits**: Each single-name vault is structured as a permissionless smart contract that accepts USDC deposits. This means anyone can participate in liquidity provision by simply depositing funds, democratizing access and decentralizing liquidity sources across multiple participants. These deposits provide the capital the vault requires to make markets for the designated asset.

**Pricing Mechanism**: The vaults use the dYdX Chain’s on-chain price index (typically derived from external oracle data) as a fair value reference. This index price, combined with the vault's internal inventory and capital, allows the vault to automatically generate a mid-price around which it quotes bids and offers. By automating fair value determination and spreads, the vault maintains a predictable and transparent approach to market-making, reducing manual intervention and operational overhead.

**Automated quote generation**: Leveraging the fair value, each vault is programmed to place multiple bids and offers on either side of the mid-price. This ensures a stable order book presence that provides immediate liquidity for both buyers and sellers. The quoting strategy is predefined within the vault’s smart contract, ensuring it is consistently enforced without human intervention.

**Risk management**: The vaults are designed to self-balance based on inventory and capital, automatically adjusting quotes as necessary to mitigate risk. If inventory builds up on one side of the market, the vault adjusts its mid price accordingly to manage risk exposure. This reactive approach enables the vault to maintain lower risk and remain effective over time, providing continuous liquidity even in volatile market conditions.

**Protocol integration and uptime**: As a protocol-native solution, single-name vaults are enshrined within the dYdX Chain architecture. This integration ensures the vaults operate with minimal downtime, leveraging the chain’s uptime and validator support. The decentralized nature of the dYdX Chain also means that liquidity provision does not depend on any single centralized market maker or infrastructure provider, further securing the vaults’ role in the ecosystem.

In summary, the single-name vaults architecture transforms liquidity provision into a decentralized and cost-effective mechanism. By aligning the vaults directly with the dYdX Chain protocol, they enable round-the-clock liquidity provision without the ongoing expense of external market-making services.

Of course, while this architecture is theoretically interesting, there are failure modes. For instance, latency is key for market-making, and the vault's latency in updating fair value of an instrument is atrocious (order of seconds of latency) compared to high-frequency trading firms' latency (order of millisecond(s) of latency). Furthermore, vaults' quoting did not account for recent volatility, nor was there a research and parameter optimization process based on post-trade data. With this in mind, it was not a certainty that vaults would be effective when starting this experiment. Hence, instead of theorizing, we as the dYdX community put our money where our mouth was and tried running the vaults in prod!

## Experimental approach

Our experimental approach here was rather simple: allocate capital among many of the markets on dYdX, in reasonably small size (\$5k-\$50k per market), and observe the profitability of each of the markets. With sufficient live trading data, it should be quite evident how profitable (or unprofitable) the vaults are, which can be used to inform the business decision on whether they should be utilized as a liquidity cornerstone for the protocol long term.

Starting in June, we allocated to 118 markets, ranging from main names like BTC-USD, all the way to 'wtf is this thing' names. The vaults are still running and providing liquidity to this day on most of the deployed names (with the exception of a few vaults that were liquidated).

## Results

Here is the total profit and loss (PnL) that came from each vault after fees.

![post-fee-pnl](/Users/max/Desktop/dydx_project/figures/post-fee-pnl.png)

There are some big numbers here, and it's *quite* tailed, with the top two best and worst outcomes generating a lot of the sum of absolute PnL's. We see that a typical market has a slightly-negative PnL, which is to be expected of a simple market-making vault. We expect that liquidity provision on the exchange will be slightly -EV, but the question is *is market making on the exchange lower EV than a market maker agreement?* To answer that, we have the below graph of the cost of liquidity to the protocol on each market.

![cost-of-liquidity](/Users/max/Desktop/dydx_project/figures/cost-of-liquidity.png)

Again, this graph has quite the tail, where we see that the TRUMPWIN market had massive cost per month. This is in part due to the fact that (a) the TRUMPWIN market only operated for a month, (b) it is a binary market which is fundamentally higher volatility, and (c) the pricing oracle (prediction market prices) is a bit more bespoke than standard asset pricing oracles available for most of the perps tokens.

Overall, we have the following metrics for the entire experiment period.

| Metric                                   | Value                |
| ---------------------------------------- | -------------------- |
| Total cost of liquidity across markets   | $58,549.97 / month   |
| Avg. cost of liquidity single market     | $500.43 / month      |
| Stdev cost of liquidity single market    | $3,123.95 / month    |
| Stdev of total monthly cost of liquidity | $33,790.71 / month   |
| Ann. exp. total cost of liquidity        | $702,599.61 / year   |
| Stdev of total annual cost of liquidity  | $117,054.45 / year   |
| 3 Stdev annual cost of liquidity         | $1,053,762.96 / year |

This is approximating what the annual cost would be for providing liquidity on the 117 markets. For reference, the dYdX ecosystem was paying \$2,500/month/market for liquidity before utilizing the vaults, and is paying on average ~\$500/month/market with vaults, just over a quarter of the previous spend.  In a 3-stdev year, the community would be paying just over \$1M for liquidity on these 117 markets. All things considered, vaults were *extremely cheap* form of liquidity.

Interestingly, we can use these estimates to determine how much revenue share a mega-vault would need to receive from the protocol if it were to quote these markets. If we want the MegaVault to be PnL neutral, while quoting in exactly in the configuration that we did in this experiment, then it would need to receive \$62,000 in revenue share per month. If we assume the protocol does ~\$200M/day in volume, that the average (maker+taker) fee for a trade is (-1.1bp + 2.5bps) = +1.4bps, then the protocol generates about \$850k/month in revenue. In this world, the protocol would only need to share \$62k/month to make the megavault PnL neutral, i.e., only a 7.3% revenue share. If we wanted to make the megavault profitable at 3stdev (roughly equivalent to a 3 Sharpe ratio), then we would need to do a 11.3% revenue share to the megavault. Of course, this analysis is based off of quoting exactly as we did (117 markets with the same capital allocations and the same parameters). A megavault would likely want to quote more markets, in larger size, so it's likely that it requires a larger revenue share.

## What's next for vaults?

The dYdX Chain v7.0 software release included a *megavault*, which is a vault that will be actively managed by a third-party operator. This megavault will deploy liquidity across many names, thus benefitting from unified cross-margining and attentive risk management. See [this governance proposal](https://dydx.forum/t/drc-proposal-for-dydx-unlimited-v7-0-0-protocol-upgrade/3125) for more details on the megavault architecture.

## Recommendations

**Send it.** The cost for liquidity here is a fraction of that which it would cost to engage designated market makers. Our estimates put the required cost of liquidity at around \$525.43/market/month. If we want to make the megavault appealing with a high Sharpe ratio, then we can give a ballpark of 11.3% revenue share to the megavault.

**Prediction Market Quoting Improvements.** On prediction markets that have a known time-to-expiry, we really should try to estimate the volatility and work that into the mid price for the quoting. Putting on a \$100k TRUMPWIN position at ~60-40 odds four days before the election has an annualized vol per unit of leverage of $\sqrt{0.6*0.4} \cdot \sqrt{\frac{365}{4}} \approx 468\%$. For reference, BTC has annual vol of around 40-60%, and PEPE rarely exceeds 150% annual vol (with just a week ago being one of those exceptions, :). Perhaps even more generally, markets could have a measurement of the recent volatility of the index, then factor this into the quoting, increasing the urgency with which the vault exits risk via moving its fair price more aggressively out of risk.






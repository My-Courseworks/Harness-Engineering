# Scratch 03: End-to-end agent deployments from OpenAI, Anthropic and practitioner sources (sweep of 2026-10-26)

These are working notes that seed the agentic system-design catalogue. Each entry is a real deployment, or a named pilot, in which an LLM agent plans and acts over several steps toward a business outcome.

## Method and caveats

- **Fetching.** Every URL cited below was fetched during this sweep. Quotes are 25 words or fewer and were taken from the fetched page. The fetch tool sometimes summarises, so I asked for the exact text when re-checking the quotes that matter most.
- **openai.com was blocked.** Every `openai.com/index/...` and `help.openai.com` page returned HTTP 403 to the fetcher, and I did not try to get around the block. OpenAI-side deployments are therefore cited through the partner's own page (Stripe, Instacart, Ramp), through trade press, or through `developers.openai.com`, which did load. Where an OpenAI primary page exists, it is named as "primary (403, not read)".
- **Numbers are mostly self-reported.** Almost every scale or impact figure comes from the vendor or the deployer. Projections are marked as projections.
- **Fields in each entry.** Deployer / vendor, date, URL, quote, the end-to-end flow, scale, the hardest constraints, and the classic system-design problem it parallels.

---

## A. Agentic commerce: an agent buys on a user's behalf

### A1. ChatGPT Instant Checkout and the Agentic Commerce Protocol (ACP), plus the 2026 walk-back
- **Deployer / vendor.** OpenAI (ChatGPT) and Stripe (payment processor). Launch merchants were US Etsy sellers, with "over a million Shopify merchants" announced as coming soon.
- **Dates.** Launched 2025-09-29. Changed course 2026-03-25.
- **URLs.**
  - https://stripe.com/newsroom/news/stripe-openai-instant-checkout
  - https://www.agenticcommerce.dev/
  - https://retaildive.com/news/walmart-sparky-chatgpt-instant-checkout/815647/
  - Primary (403, not read): openai.com/index/buy-it-in-chatgpt/
- **Quote.** "ChatGPT acts like the buyer's AI agent, helping them buy from businesses just like a personal shopper would." (Stripe)
- **End to end.**
  1. The user states a shopping intent in chat, and ChatGPT discovers and ranks products.
  2. The merchant exposes an ACP checkout over REST or MCP.
  3. Stripe issues a Shared Payment Token (SPT) that is "limited to a specific merchant and basket total."
  4. ChatGPT passes the token to the merchant. The merchant can accept or decline the order, charges the payment method, calculates and remits tax, and handles fulfilment and returns. It can still use Stripe Radar fraud scores.
- **Who is merchant of record.** The business stays merchant of record (agenticcommerce.dev).
- **Human in the loop.** The user completes payment in the chat with a chosen method, such as Link.
- **The 2026 walk-back.** OpenAI said it "found that the initial version of Instant Checkout did not offer the level of flexibility that we aspire to provide." Merchants may now use their own checkout, and ACP was extended to product discovery. Target, Sephora, Nordstrom, Lowe's, Best Buy, The Home Depot and Wayfair have integrated with the protocol (Retail Dive, 2026-03-25).
- **Hardest constraints.**
  - Money movement through a credential delegated to the agent.
  - Three parties to coordinate: the agent platform, the merchant and the payment processor.
  - Merchant-of-record liability.
  - Returns and disputes.
  - The checkout ownership the platform gave back.
- **Parallel.** Design Amazon checkout, except that the storefront is someone else's agent.

### A2. Instacart app in ChatGPT with full checkout
- **Deployer / vendor.** Instacart, built on the OpenAI Apps SDK with Instant Checkout and ACP.
- **Date.** 2025-12-08.
- **URL.** https://www.supermarketnews.com/grocery-technology/instacart-launches-end-to-end-shopping-app-on-chatgpt
- **Quote.** Users can "approve the AI-generated list and pay for it all within the ChatGPT platform."
- **End to end.** A recipe or meal plan becomes a shopping list. The agent maps the list to products, the user approves it, and payment happens inside ChatGPT. Instacart shoppers then fulfil the order.
- **Human in the loop.** The user approves the list before paying.
- **Scale.** No figures were given. Instacart said it was the first app with checkout inside ChatGPT (a company claim).
- **Hardest constraints.**
  - Inventory and price freshness at the moment of checkout.
  - Substitutions after the user has approved.
  - Splitting each order across retailers.
- **Parallel.** Design Swiggy Instamart or DoorDash, where the cart is built by an agent.

### A3. Walmart: Instant Checkout first, then its own Sparky agent as a ChatGPT app
- **Deployer / vendor.** Walmart and Sam's Club, with OpenAI.
- **Dates.** 2025-10-14, then 2026-03-25.
- **URLs.**
  - https://www.retaildive.com/news/walmart-openai-chatgpt-shopping-instant-checkout/802708/
  - https://retaildive.com/news/walmart-sparky-chatgpt-instant-checkout/815647/
- **Quote.** Instant Checkout "plans to expand to multi-item carts." (2025: single items only)
- **End to end.**
  - Version 1 (2025): purchase of a single item inside ChatGPT. Merchants pay a fee on each purchase.
  - Version 2 (2026): Walmart's own commerce agent, Sparky, runs as a ChatGPT app. It goes "from product discovery in ChatGPT into a Walmart environment" that handles account linking, loyalty and payment.
- **Hardest constraints.**
  - Who owns the customer's identity and loyalty account: the platform or the merchant.
  - Multi-item carts.
  - Fees charged to the merchant.
- **Parallel.** Amazon or Walmart checkout where the agent and its runtime belong to the merchant.

### A4. Shopping with UPI inside ChatGPT (India): NPCI, Razorpay and OpenAI
- **Deployer / vendor.** NPCI (the UPI rails operator), Razorpay (merchant integration) and OpenAI. Merchants were BigBasket and Vi. Banks were Axis Bank and Airtel Payments Bank.
- **Date.** 2025-10-09 (pilot).
- **URL.** https://techcrunch.com/2025/10/09/india-pilots-ai-chatbot-led-e-commerce-with-chatgpt-gemini-claude-in-the-mix
- **Quote.** "users will pre-authorize the amount transacted through chatbots through two-factor authentication."
- **End to end.**
  1. The user asks for something, such as groceries for a recipe or a mobile recharge.
  2. The agent searches the merchant's catalogue and builds the order.
  3. **UPI Reserve Pay** earmarks funds for future debits to approved merchants.
  4. **UPI Circle** delegates authentication so that payment completes inside the chat.
  5. Razorpay settles the payment.
- **Data access.** Razorpay says AI companies do not see payment data.
- **Scale.** UPI handles over 20 billion transactions a month. Razorpay has completed proofs of concept with Gemini and Claude.
- **Hardest constraints.**
  - Delegated authority over a real-time payment rail that cannot be reversed.
  - Pre-authorised spend limits.
  - Regulated rails, with two-factor authentication required.
- **Parallel.** Design UPI or a digital wallet, where the payer is an agent acting under mandates.

### A5. Swiggy MCP servers (Food, Instamart, Dineout) used from ChatGPT, Claude and Gemini
- **Deployer / vendor.** Swiggy, exposing its services as MCP servers for third-party assistants.
- **Dates.** Launched 2026-01-27. Hands-on test 2026-01-28 (updated 2026-03-21).
- **URL.** https://www.medianama.com/2026/01/223-ordering-chatgpt-swiggy-services-working/
- **Quote.** "The integration is real, but gated."
- **End to end.**
  - The assistant reads the user's saved addresses, searches restaurants and groceries, builds carts, and starts checkout or a Dineout reservation.
  - Login uses Swiggy's OTP flow.
  - In ChatGPT it required developer mode and a separate MCP URL for each vertical.
- **What the hands-on test found.**
  - Orders placed by the AI were **cash on delivery only**, and online payment was blocked.
  - Instamart checkout was not exposed.
  - Some menus failed to load.
- **Hardest constraints.**
  - Authenticating the user on the merchant's side from inside a third-party agent.
  - Keeping payment off the agent path; cash on delivery was the merchant's de-risking choice.
  - Catalogue reliability.
- **Parallel.** Design Swiggy or DoorDash with the frontend replaced by an MCP surface.

### A6. OpenAI Operator, and ChatGPT apps from Uber and DoorDash
- **Deployer / vendor.** OpenAI. Launch partners for Operator were DoorDash, Instacart, OpenTable, Priceline, StubHub, Thumbtack and Uber.
- **Dates.** Operator launched 2025-01-23. Apps for Uber and Uber Eats were announced 2025-10-06.
- **URLs.**
  - https://www.constellationr.com/blog-news/insights/openai-launches-operator-eyes-ai-agents-without-apis
  - https://www.restaurantdive.com/news/chatgpt-instacart-doordash-uber-target-grocery-delivery/802604
- **Quote.** "Operator asks the user to takeover when it needs more information and credentials."
- **End to end.**
  - **Operator.** A Computer-Using Agent drives ordinary websites through screenshots and simulated mouse and keyboard, with no API. It hands control back to the user for logins and credentials, asks for confirmation before actions, and declines sensitive tasks.
  - **Uber Eats app.** The app confirms the delivery address and shows restaurants and menus. Then "ChatGPT will then prompt users to launch the Uber Eats app to complete their orders."
- **Hardest constraints.**
  - Acting on someone's behalf on sites built for humans.
  - Session and credential handoff.
  - Deciding where the irreversible step happens, which here was handed back to the partner's app.
- **Parallel.** Design Uber or DoorDash ordering when the client is an agent.

### A7. Anthropic Project Deal: an internal marketplace where agents traded with agents
- **Deployer / vendor.** Anthropic, with 69 employees in its San Francisco office.
- **Dates.** Ran December 2025. Published 2026-04-24.
- **URL.** https://www.anthropic.com/features/project-deal
- **Quote.** "all of the deals were conducted by AI models acting on our employees' behalf."
- **End to end.**
  1. Claude interviews each employee about what to sell and buy, price limits and negotiating style.
  2. The answers become a custom system prompt for that person's agent.
  3. Agents post listings, make offers, counter and close deals in Slack. Each person had a $100 budget, settled afterwards as a gift card.
- **Human in the loop.** None: "The agents didn't go back to their humans to sign off on a deal."
- **Scale.** 186 deals, just over $4,000, more than 500 listings.
- **Findings.**
  - Opus agents sold for about $2.68 more per item and bought for about $2.45 less than Haiku agents.
  - People represented by Haiku rated their deals as fair just as often, so they did not notice the gap.
  - Agents sometimes made up details.
- **Hardest constraints.**
  - Negotiating between agents on behalf of principals.
  - Fairness when the two sides run models of different strength.
  - Settlement.
  - Prompt injection between counterparties.
- **Parallel.** Design Craigslist, OLX or Facebook Marketplace where both buyer and seller are agents.

### A8. Reference architecture, not a single deployment: Anthropic's commerce agents blueprint
- **Vendor.** Anthropic. Named partners are Shopify (a reference storefront using UCP and Shop Sign-in), Priceline, Square, Zomato, Wix, Intuit, Visa, Mastercard and Accenture.
- **Date.** 2026-09-02.
- **URL.** https://claude.com/blog/claude-for-commerce-agents
- **Quote.** "When the agent proactively suggests a change, a person approves it before anything goes live."
- **End to end.** There are two halves:
  - A **shopping agent** inside the retailer's app searches the catalogue, plans multi-item requests, builds the cart and hands off to checkout. It also handles order status and returns.
  - A **merchant agent** covers analytics, inventory, and pricing and promotion proposals. A human approves its changes.
- **Payment.** Left to the merchant or to an agentic payments provider.
- **Stated results.** Carts up to 35% larger and 60% more likely to complete. These are vendor claims.

---

## B. Payments initiated by agents, as card networks and banks see them

### B1. Visa Intelligent Commerce goes live across Europe
- **Deployer / vendor.** Visa, with more than 30 European issuers that completed live transactions (including Barclays, HSBC UK, Revolut, BBVA, ING and Klarna). Merchants included lastminute.com, Frasers, Cleverbridge and BrickDepot. Cloudflare and Akamai support the merchant side.
- **Date.** 2026-07-02.
- **URL.** https://www.mynewsdesk.com/uk/visa/pressreleases/visa-and-banks-across-europe-reach-the-next-phase-of-agentic-commerce-unlocking-secure-access-to-merchants-3457328
- **Quote.** "with AI agents now transacting based on cardholder instructions directly with independent merchants."
- **End to end.**
  - Agents buy on merchant websites within limits the consumer set.
  - Each transaction is authenticated with Visa Payment Passkeys, which ties it to a verified user and their explicit instruction and satisfies EU Strong Customer Authentication.
  - The Trusted Agent Protocol (TAP) and Visa's Agent Directory let merchants tell verified agents apart from bot traffic.
- **Hardest constraints.**
  - Strong Customer Authentication regulation.
  - Proving the agent's identity to a merchant it has never dealt with.
  - Recording the consumer's mandate for disputes.
- **Parallel.** Design a card-network authorisation path in which the agent is a new party.

### B2. Visa and Aldar (UAE): a voice agent pays real-estate service charges
- **Deployer / vendor.** Aldar (property developer, Live Aldar app), Visa, and Emirates NBD (card issuer).
- **Date.** 2025-12-18.
- **URL.** https://www.visa.com/en-ae/newsroom/visa-aldar-agentic-payments-partnership
- **Quote.** "Visa Intelligent Commerce can support trusted, secure agent-initiated transactions on the Visa cardholder's behalf."
- **End to end.** The resident speaks to the agent in the app. The agent walks through the steps, confirms details with the user, and completes the service-charge payment "within seconds." Visa's Token Management Service tokenises the card.
- **Planned next.** Personalised offers and automatic application of loyalty points.
- **Hardest constraints.**
  - Authorisation by voice, with consent captured through the conversation.
  - Recurring property dues.
- **Parallel.** Design a bill-payment or wallet system with voice as the interface.

### B3. Mastercard Agent Pay: first live agentic transaction in Singapore, a ride booking
- **Deployer / vendor.** Mastercard, with DBS and UOB. CardInfoLink's agent booked through hoppa, a mobility marketplace.
- **Date.** Announced 2026-03-04 (article dated 2026-03-10).
- **URL.** https://www.artificialintelligence-news.com/news/mastercard-agentic-payments-singapore-dbs-uob/
- **Quote.** "tokenisation, passkey authentication, and explicit consent layers from the outset."
- **End to end.** The agent books an airport transfer to Changi. A Mastercard Agentic Token, issued to that specific agent, carries the payment. The consumer's consent is captured explicitly, and a Payment Passkey confirms the purchase.
- **Hardest constraints.**
  - Credentials scoped to one agent.
  - A trail showing what the cardholder actually authorised.
- **Parallel.** Design Uber or Grab payments in which the caller is an agent.

---

## C. Travel and mobility booking

### C1. Priceline Penny, rebuilt on Claude
- **Deployer / vendor.** Priceline (Booking Holdings), with Anthropic Claude. Google Cloud and OpenAI support search and voice.
- **Date.** 2026-06-05.
- **URL.** https://www.hoteldive.com/news/priceline-travel-booking-agentic-ai-penny/822647/
- **Quote.** "Customers can purchase flights without having to leave the Priceline platform."
- **End to end.**
  - A natural-language trip request is handled by "over 10 specialized agents as a coordinated system": flights, hotels, cars, recommendations and service.
  - The agents check live pricing and availability, explain tradeoffs, and book inside the conversation. They also support existing reservations.
- **Human in the loop.** Not described in the article.
- **Scale.** About 10 minutes saved per trip compared with calling support. Higher conversion was claimed but not quantified.
- **Hardest constraints.**
  - Inventory and prices that go stale between quote and book.
  - Multi-leg bookings that must succeed together or not at all.
  - Fare rules and cancellations.
  - Splitting work across more than 10 agents.
- **Parallel.** Design Expedia or MakeMyTrip, where the itinerary is planned by an agent.

### C2. Expedia and Booking.com apps in ChatGPT (agent does discovery, merchant does the booking)
- **Deployer / vendor.** Expedia and Booking.com, built on the OpenAI Apps SDK over MCP.
- **Date.** 2025-10-06 (article updated 2025-10-07).
- **URL.** https://upgradedpoints.com/news/expedia-booking-apps-live-inside-chatgpt/
- **Quote.** "Once confirmed, your reservations appear in the "Trips" section of your Expedia account."
- **End to end.** A conversational search returns live prices, photos and availability in the chat. The user then **clicks through to the partner site** to book and pay.
- **Why it is here.** It is a contrast case: the travel agencies kept the irreversible step and the customer relationship on their own sites.
- **Hardest constraints.**
  - Fees, taxes and cancellation terms are hidden in the chat view (per TourMaG coverage).
  - Loyalty benefits may not carry through.

(Mastercard's hoppa ride booking, B3, also belongs to mobility.)

---

## D. Retail operations, merchandising and marketplace sellers

### D1. Anthropic Project Vend, phases 1 and 2: Claude runs a shop
- **Deployer / vendor.** Anthropic's Frontier Red Team and Andon Labs.
- **Dates.** Phase 1 2025-06-27. Phase 2 2025-12-18.
- **URLs.**
  - https://www.anthropic.com/research/project-vend-1
  - https://www.anthropic.com/news/project-vend-2
- **Quote.** "Your task is to generate profits from it by stocking it with popular products that you can buy from wholesalers."
- **Phase 1.**
  - Claudius (Sonnet 3.7) chose stock, found suppliers through web search, emailed wholesalers and requested labour through a simulated email tool, kept notes on its balance, talked to customers in Slack, and set the checkout prices.
  - Humans at Andon Labs restocked the shelves.
  - It lost money. It sold below cost (the metal cubes), gave in to discount requests, gave customers a wrong payment account, and had a confused episode in which it claimed to be human.
- **Phase 2.**
  - Three agents: Claudius (Sonnet 4.0, later 4.5), Seymour Cash as a CEO agent with an objectives-and-key-results tool, and Clothius for merchandise.
  - New tools: a CRM, inventory records with purchase cost, a browser, payment links, and Google Forms.
  - Claudius had no payment interface, so it needed a human to buy stock.
  - Expanded to New York and London. Weeks with negative margin "largely eliminated."
  - The CEO agent approved lenient requests about 8 times as often as it denied them, because it shared Claudius's blind spots. Requiring Claudius to check prices and delivery times did more good than pressure from above.
- **Hardest constraints.**
  - Margin discipline when customers try to manipulate it.
  - Long-horizon state.
  - Supervision by a second agent on the same model.
  - Spending power gated by a human.
- **Parallel.** Design a vending machine, kiosk or small retail point of sale, run by an agent.

### D2. Amazon Seller Assistant becomes agentic
- **Deployer / vendor.** Amazon, on Bedrock, using Amazon Nova and Anthropic Claude.
- **Date.** 2025-09-17.
- **URL.** https://www.aboutamazon.com/md/news/innovation-at-amazon/seller-assistant-agentic-ai
- **Quote.** "If the seller approves, Seller Assistant implements the solution and clears the warning before it becomes a problem."
- **End to end.**
  - Continuously monitors account health, FBA inventory and compliance, such as missing UL certificates or products that may count as pesticides.
  - Flags slow-moving stock, and proposes markdowns or removals.
  - Prepares shipment plans across FBA and Amazon Warehousing and Distribution.
  - Coordinates promotions.
- **Human in the loop.** It acts only after the seller approves.
- **Scale.** Available to all US sellers. More than 90% of selling partners worldwide have access in their own language.
- **Hardest constraints.**
  - Acting on the seller's account with delegated authority.
  - Regulatory compliance in every country the seller sells to.
  - Storage fees that grow with time.
- **Parallel.** Design Amazon Seller Central with an operations agent.

### D3. Revionics multi-agent pricing system (Google ADK)
- **Deployer / vendor.** Revionics (retail pricing), on Google's Agent Development Kit. No retailers were named.
- **Dates.** Alpha shown at Next 2025. Generally available 2026-04-22.
- **URL.** https://revionics.com/blog/revionics-multi-agent-pricing-system-is-now-ga-heres-what-that-means-for-retail
- **Quote.** "One agent surfaces competitive gaps. Another models the financial impact of closing those gaps."
- **End to end.**
  1. A pricing manager asks a question such as "which categories are most exposed to competition?"
  2. Agents find at-risk SKUs, forecast the effect of a change, then apply the retailer's business and margin rules and execute the price changes. The post says changes can be pushed in real time.
- **Human in the loop.** An approval step is not described.
- **Hardest constraints.**
  - Price changes that reach every store and online shopper.
  - Margin guardrails.
  - Forecast error.
- **Parallel.** Design dynamic pricing (Uber surge or Amazon repricing) with a natural-language control plane.

---

## E. Procurement and supply chain

### E1. Duvo and Rohlik Group: procurement and supply-chain agents (Claude Agent SDK)
- **Deployer / vendor.** Rohlik Group (European online grocer, more than €1.5B revenue), Duvo, and Anthropic.
- **Date.** Not stated on the page (© 2026).
- **URL.** https://claude.com/customers/duvo
- **Quote.** "Duvo now monitors continuously, builds negotiation cases, and initiates supplier outreach."
- **End to end.**
  - A single run logs into a supplier portal, pulls delivery status for many purchase orders, checks them against SAP (including through the SAP GUI), flags discrepancies, and decides whether to escalate or correct.
  - It then sends follow-up emails and logs the outcome.
  - It tracks commodity-linked SKUs in five markets, monitors prices, and builds negotiation cases with suppliers.
  - It works across email and phone.
- **Human in the loop.** High-risk actions need human approval, and the decision is stored for future runs.
- **Scale.**
  - €2.8M+ annualised savings within three months.
  - Supplier negotiation cycle one month shorter, about 80% automated.
  - Inbound delivery confirmations up from 52% to 90%.
  - Product availability up from 78% to 93%.
- **Hardest constraints.**
  - Legacy ERP screens with no API.
  - Commitments to suppliers that cannot be undone.
  - Memory of earlier human decisions.
- **Parallel.** Design a procure-to-pay system where the buyer is an agent.

### E2. OpenAI's internal finance as "customer zero": PwC CFO agents, Ramp's procurement agent, and enterprise dots
- **Deployer / vendor.** OpenAI's own finance organisation, with PwC. Ramp built on AgentKit. OpenAI dots are in enterprise preview.
- **Dates.** PwC collaboration 2026-05-06. Ramp on AgentKit 2025-10-06. dots 2026-10-02.
- **URLs.**
  - https://itbrief.co.uk/story/openai-and-pwc-build-finance-ai-agents-for-cfo-teams
  - https://venturebeat.com/ai/openai-unveils-agentkit-that-lets-developers-drag-and-drop-to-build-ai
  - https://itbrief.co.uk/story/openai-launches-dots-always-on-ai-agents-for-work
  - Primaries (403, not read): openai.com/index/openai-pwc-finance-collaboration/ and openai.com/index/introducing-dots/
- **Quotes.**
  - "A procurement agent is being built for internal use."
  - "Specialist dots would operate with their own identities, credentials and system access."
- **End to end.**
  - **PwC and OpenAI.** Agents across planning, forecasting, procurement, payments, treasury, tax and the close. Codex let OpenAI's finance team handle five times as many contracts with the same headcount.
  - **Ramp.** Built a procurement agent with Agent Builder "in two sprints rather than two quarters." No functional detail was published. OpenAI is winding down Agent Builder after 2026-11-30.
  - **dots.** Always-on agents, each on its own cloud computer. The specialist enterprise version gets its own organisational identity and credentials, plus tools and approval processes the organisation defines. OpenAI tested them internally on procurement and invoice processing. Governance runs through Microsoft Agent 365.
- **Hardest constraints.**
  - Giving an agent its own identity and credentials instead of borrowing a human's.
  - Controls over spending money.
  - Making token spend visible to the CFO.
- **Parallel.** Design an approval workflow such as Coupa, where the requester is an agent with a service identity.

---

## F. Finance operations: accounts payable, invoicing, payroll and transfers

### F1. Ramp Agents for AP
- **Deployer / vendor.** Ramp. The model vendor was not named.
- **Date.** 2025-10-07.
- **URL.** https://ramp.com/blog/ramp-ap-agents-announcement
- **Quote.** "Agents surface them and input card details directly in the vendor's payment portal."
- **End to end.**
  1. On intake, the agent gathers context: vendor contracts, email history, earlier payments and POs.
  2. It assigns GL codes line by line, learning from accounting history.
  3. It screens each bill against more than 60 fraud signals.
  4. It writes an approval summary and recommendation.
  5. For vendors that accept cards, it enters the card in the vendor's portal itself.
- **Human in the loop.** Approvers read the summary and make the final decision.
- **Scale.**
  - About 85% of fields coded correctly on the first try.
  - 90,000 approval recommendations, 90% accepted.
  - $1M+ of fraud caught before routing.
- **Hardest constraints.**
  - Paying out money by typing a card into a third-party portal.
  - Catching fraud before approval.
  - Accounting accuracy.
- **Parallel.** Design Bill.com or an AP system.

### F2. Qonto: agents for small-business financial admin (Claude on Bedrock)
- **Deployer / vendor.** Qonto (more than 600,000 European SMBs), using Claude on Amazon Bedrock.
- **Date.** Not stated. The project started November 2025, and the first agent shipped about six weeks later.
- **URL.** https://claude.com/customers/qonto
- **Quote.** "Any action with a financial or customer relationship impact requires user confirmation."
- **End to end.**
  - An operator agent routes each request to a specialised agent.
  - **Payroll.** A pay slip and transfer per employee, reviewed in one bulk batch.
  - **Invoices.** Drafted per client from an uploaded CSV.
  - **Transfers.** Beneficiary, amount and reference filled in.
  - An analyst agent answers questions about cash flow.
  - Sensitive flows add deterministic checks. Opus, Sonnet or Haiku is chosen by task complexity.
- **Scale.**
  - Transfers delegated up to €100,000.
  - One batch of more than 500 invoices.
  - Transfers 2× faster, invoices 3×, payroll 5×.
- **Hardest constraints.**
  - Bank transfers that cannot be undone.
  - Confirming a batch without the user approving every item by reflex.
  - Bank-grade regulation.
- **Parallel.** Design a bank payout or bulk-transfer system with an agent preparing the batch.

### F3. Intuit QuickBooks agents: payments, accounting, finance and customer
- **Deployer / vendor.** Intuit. The model vendor was not named.
- **Date.** 2025-07-01.
- **URL.** https://investors.intuit.com/news-events/press-releases/detail/1258/intuit-introduces-ground-breaking-virtual-team-of-ai-agents-to-fuel-growth-for-businesses
- **Quote.** "Optimizes and grows cash flow by getting businesses paid an average of 5 days faster"
- **End to end.**
  - **Payments Agent.** Predicts late payment, then creates and sends invoices and reminders.
  - **Accounting Agent.** Categorises transactions and helps reconcile.
  - **Customer Agent.** Finds leads, drafts replies and schedules meetings.
- **Human in the loop.** Human experts are available only through QuickBooks Live. A required approval step is not described.
- **Scale.** Up to 12 hours a month saved. Paid 5 days faster (beta cohort).
- **Hardest constraints.**
  - Collections messages going out to the merchant's own customers.
  - Books that must be accurate.
- **Parallel.** Design Splitwise or invoicing with automatic reminders, at small-business scale.

### F4. Dow: freight invoice audit agent (Microsoft Copilot Studio)
- **Deployer / vendor.** Dow, using Microsoft Copilot Studio and Copilot.
- **Date.** 2024-11-13.
- **URL.** https://www.microsoft.com/en-us/worklab/ai-impact-at-dow-copilot-identifies-millions-in-cost-savings
- **Quote.** An autonomous agent "monitors incoming email for attached PDF invoices" and structures the data for analysis.
- **End to end.**
  1. An autonomous agent watches the inbox, extracts data from PDF invoices, and flags billing anomalies on a dashboard.
  2. A second "Freight Agent" lets staff question the flagged data in natural language.
- **Human in the loop.** A dispute or recovery flow is not described.
- **Scale.**
  - More than 100,000 PDF invoices a year, and up to 4,000 shipments a day.
  - The pilot covered 43,000 shipments.
  - "Millions" in first-year savings is a projection.
- **Hardest constraints.**
  - Extracting data from messy PDFs.
  - Deciding which flagged anomalies are worth recovering.
- **Parallel.** Design freight-audit or expense-audit pipelines.

---

## G. Financial crime, KYC/AML and fintech risk operations

### G1. FIS AML Investigations Agent (Claude), first deployed at Amalgamated Bank
- **Deployer / vendor.** FIS (core-banking vendor) and Anthropic. Amalgamated Bank is the design partner.
- **Dates.** Announced May 2026. Commercially available 2026-10-15.
- **URLs.**
  - https://www.fisglobal.com/about-us/media-room/press-release/2026/fis-aml-investigations-agent-now-commercially-available
  - https://www.anthropic.com/news/finance-agents
- **Quote.** "every output is a recommendation, no case can be closed without explicit analyst confirmation."
- **End to end.**
  1. **Level 1 triage.** Compares each alert against the customer's type, history and expected behaviour.
  2. **Level 2 investigation.** Assembles evidence from core banking, payments and data systems, integrating natively with FIS Horizon and Systematics. Every statement links to its source record or check image.
  3. Drafts the SAR (suspicious activity report) narrative for the analyst.
  4. Logs the analyst's decision and the agent's reasoning to an audit trail.
- **Isolation.** Each bank's risk logic and thresholds are kept isolated through the FIS Control Plane.
- **Scale (projections from Amalgamated's own analysis).** Level 1 review time down more than 90%, Level 2 investigation about 98%, SAR drafting more than 80%.
- **Related.** Anthropic's 2026-05-05 finance launch also ships a "KYC screener" agent template.
- **Hardest constraints.**
  - BSA/AML regulation.
  - Every claim must cite its evidence.
  - Tenants in a multi-bank platform must not see each other's data.
  - A human must close every case.
- **Parallel.** Design a fraud or AML case-management system.

### G2. Brex: agents for KYC, underwriting, fraud, disputes and audit, written to SOPs (Latent Space)
- **Deployer / vendor.** Brex (corporate cards). The model vendors were not named.
- **Date.** Page dated "Jan 17" without a year; its copyright is 2026, so probably 2026-01-17.
- **URL.** https://www.latent.space/p/brexs-ai-hail-mary-with-cto-james
- **Quote.** "breaking work into auditable, repeatable steps unlocked faster automation in KYC, underwriting, fraud, and disputes."
- **End to end.**
  - Agents follow written procedures (SOPs) across onboarding KYC, credit underwriting, fraud and disputes.
  - The audit-agent pattern splits detection, judgment and follow-up into separate agents.
  - An executive-assistant agent coordinates specialist agents for policy, travel and reimbursement.
- **Scale.** "shipping production agents to 40,000+ companies."
- **Hardest constraints.**
  - Regulated decisions about credit and identity.
  - Keeping the agent's reasoning auditable.
- **Parallel.** Design onboarding and underwriting at a card issuer.

---

## H. Insurance claims and underwriting

### H1. Allianz Project Nemo: seven agents settle food-spoilage claims
- **Deployer / vendor.** Allianz Australia. The model vendor is not stated.
- **Dates.** Live July 2025. Article 2025-11-03.
- **URL.** https://allianz.com/en/mediacenter/news/articles/251103-when-the-storm-clears-so-should-the-claim-queue.html
- **Quote.** "The planner agent starts the workflow, overseen by the cyber agent to ensure data security."
- **End to end.** Claims under AUD 500 are handled by seven agents:
  - **Planner** starts the workflow.
  - **Cyber** oversees data security throughout.
  - **Coverage** checks that the policy covers food spoilage after severe weather.
  - **Weather** confirms that a matching weather event happened.
  - **Fraud** looks for signs of fraud.
  - **Payout** works out the amount.
  - **Audit** summarises all the decisions for a human.
- **Human in the loop.** A claims professional makes the final payout decision. Payouts are never automated.
- **Scale.** Several days cut to one day, sometimes hours. Filing to human review in under 5 minutes. An 80% cut in processing and settlement time.
- **Hardest constraints.**
  - Money going out.
  - Insurance regulation.
  - Correlated surges, since a storm triggers thousands of claims at once.
  - Checking claims against an external source (weather data).
- **Parallel.** Design an insurance claim pipeline that has to absorb catastrophe spikes.

### H2. Allianz and Anthropic: claims agents for motor and health insurance
- **Deployer / vendor.** Allianz and Anthropic.
- **Date.** 2026-01-09 (early-stage projects).
- **URL.** https://allianz.com/en/mediacenter/news/media-releases/260109-allianz-and-anthropic-forge-global-partnership.html
- **Quote.** "Allianz and Anthropic are developing custom AI agents capable of orchestrating multi-step workflows"
- **End to end.** Agents handle intake documentation through to claims processing, aiming for faster first payments. The partners are co-developing an audit layer that records each decision, its rationale and its data sources.
- **Human in the loop.** "Especially in sensitive or very complex cases, Allianz employees take over."
- **Scale.** None reported yet.

### H3. DXC Assure: Claude in an insurance processing backbone
- **Deployer / vendor.** DXC Technology (14,000-person insurance business), on the Claude Platform API.
- **Date.** Not stated (© 2026).
- **URL.** https://claude.com/customers/dxc
- **Quote.** "a document lands, and Claude classifies its type in under a second."
- **End to end.**
  - **Document intelligence.** Classifies documents and extracts policy, party, amount and date.
  - **Underwriting.** Structures each submission and presents exceptions to underwriters.
  - **Workflow.** Routes decisions to the right people.
  - **Smart Apps.** Single-purpose agents, such as first notice of loss, reserving, and the workers' comp pre-injury average weekly wage calculation that sets weekly benefits.
  - **Compliance.** Every action is logged so a regulator can reconstruct the decision.
  - **Model routing.** Light models for triage, frontier models for long claim files.
- **Human in the loop.** Authority levels for agents. Humans own checkpoints with material, legal or financial impact.
- **Scale.**
  - The workers' comp app was 80% correct on the first pass. The share needing human judgment fell from 70% to 20%.
  - Embedding a new regulatory rule went from 12–18 months to days.
  - About 1% of decisions are autonomous today; the goal is 50%.
- **Hardest constraints.**
  - Benefit calculations set by statute.
  - Regulators must be able to reconstruct each decision.
  - The authority matrix.

### H4. AIG: underwriting review with Claude
- **Deployer / vendor.** AIG, with Anthropic.
- **Date.** 2025-07-15.
- **URL.** https://www.anthropic.com/news/claude-for-financial-services
- **Quote.** "we have been able to compress the timeline to review business by more than 5x in our early rollouts"
- **End to end.** Submissions are reviewed for underwriting decisions. Detail is thin.
- **Scale.** Review time 5× faster. Data accuracy up from 75% to over 90%.
- **Hardest constraints.** Pricing risk accurately, plus underwriting regulation.

---

## I. Freight brokerage and logistics dispatch

### I1. C.H. Robinson: a fleet of more than 30 agents across the shipment lifecycle
- **Deployer / vendor.** C.H. Robinson, built in-house. The model vendor was not named.
- **Date.** 2025-06-12.
- **URL.** https://www.chrobinson.com/en-us/about-us/newsroom/news/2025/ch-robinson-scales-fleet-of-ai-agents-past-30/
- **Quote.** The Orders Agent "Reads and interprets emailed tenders, including attachments, and builds orders in about 90 seconds"
- **The agents.**
  - **Quoting.** Over 1 million quotes, about 32 seconds each.
  - **Orders.** 5,500 truckload orders a day, saving 600 labour hours a day.
  - **LTL Classifier.** Assigns freight class for 2,000 shipments a day.
  - **Appointments.** More than 3,000 a day across 43,000 locations, under a minute each.
  - **Truck Posting.** Parses carrier emails into the capacity centre.
  - **Shipment Tracking.** Answers customer tracking requests.
- **Scale.** More than 3 million shipping tasks. 30% productivity gain since 2023.
- **Hardest constraints.**
  - Unstructured email input.
  - Rates and appointments that bind the company to customers and carriers.
  - High volume.
- **Parallel.** Design a freight-broker transport management system (TMS).

### I2. C.H. Robinson: agents that chase missed LTL pickups
- **Date.** 2026-01-26.
- **URL.** https://www.chrobinson.com/en-au/about-us/newsroom/press-releases/2026/chrobinson-lean-ai-agents-for-ltl-pickup-efficiency/
- **Quote.** "a new AI agent calls carriers about missed pickups and then another new AI agent decides what steps to take."
- **End to end.**
  1. A voice agent phones the carrier.
  2. A reasoning agent decides the next action, such as retendering the load.
  3. The two run up to 100 calls and 100 decisions at the same time.
- **Scale.**
  - 95% of missed-pickup checks automated, saving more than 350 hours a day.
  - Unnecessary return trips down 42%.
  - Hundreds of shipments a day across more than 11,000 customers.
- **Hardest constraints.**
  - Getting information from other companies by phone.
  - Retendering, which reassigns the load to another carrier.
  - Concurrency limits on calls.
- **Parallel.** Design a dispatch exception queue.

### I3. HappyRobot and Circle Logistics: voice agents run carrier calls for a broker
- **Deployer / vendor.** Circle Logistics (freight broker) and HappyRobot (backed by a16z).
- **Date.** Page updated 2026-09-22.
- **URL.** https://happyrobot.ai/blog/circle-logistics-x-happyrobot-case-study
- **Quote.** The AI "handles the full carrier interaction flow," including "presenting load information, negotiating rates, confirming bookings, and running fraud checks."
- **End to end.** The agent answers inbound carrier calls, presents the load, negotiates the rate, books it, and pulls compliance data to vet the carrier. It writes every field in real time to Transport Pro, DAT, Truckstop and Highway.
- **Scale.**
  - 18% of freight booked with zero human touch.
  - Manual calls down 80–100%.
  - Margin up 10%.
  - Calls answered 24/7.
- **Hardest constraints.**
  - Negotiating price on behalf of the broker.
  - Carrier fraud, such as double brokering.
  - Voice latency.
- **Parallel.** Design Uber Freight, or a load board with an agent negotiating on it.

---

## J. Legal contract negotiation and tax preparation

### J1. Luminance: autonomous contract negotiation
- **Deployer / vendor.** Luminance. Customers named on its site include AMD, EMMA Sleep and Avianca, but their use of the negotiation agent is not documented.
- **Date.** 2026-03-12 (expanded beta). Shown first in November 2023.
- **URL.** https://itbrief.co.uk/story/luminance-opens-ai-contract-tool-with-clearer-reasoning
- **Quote.** "The system sends revised drafts to counterparties, tracks responses" … "can react in real time to changes made by a counterparty's AI"
- **End to end.**
  - Reads a contract, flags risks against a playbook, and proposes redlines.
  - Sends drafts to the counterparty and tracks the replies.
  - Can negotiate with the other side's AI.
  - Each decision now shows its reasoning and the negotiation history.
- **Expansion.** Moving beyond legal teams to procurement, sales and operations for routine agreements such as NDAs.
- **Human in the loop.** Staff set the standards and do quality assurance, and can step in at any stage.
- **Hardest constraints.**
  - Binding legal commitments.
  - Negotiating against another agent.
  - Authority to sign.
- **Parallel.** Design DocuSign or a contract lifecycle management system with negotiation by agents.

### J2. TaxGPT Tax Prep Agent
- **Deployer / vendor.** TaxGPT (more than 70,000 users). The model vendor was not disclosed.
- **Date.** 2026-03-24.
- **URL.** https://www.cpapracticeadvisor.com/2026/03/24/taxgpt-releases-autonomous-tax-workflow-agent/180159/
- **Quote.** It "then opens the tax platform via browser automation, enters return data, runs diagnostics," "and flags anything that requires human judgment."
- **End to end.**
  1. Pulls W-2s, 1099s, K-1s and trial balances from folders or intake software.
  2. Drives the web-based tax software through browser automation and enters the data.
  3. Runs the software's diagnostics.
  4. Hands off to "Agent Andrew," a review agent that reconciles the return against the source documents and surfaces audit-sensitive items.
  5. A CPA signs off.
- **Scope.** Form 1040 only. Forms 1065 and 1120 are on the roadmap.
- **Scale.** 90% less first-pass prep time, about 45 minutes saved per 1040. These are vendor claims.
- **Hardest constraints.**
  - Professional liability: the CPA signs, and Circular 230 applies.
  - Driving the tax software's UI without an API.
  - The filing deadline peak.
- **Parallel.** Design TurboTax with an agent preparing the return.

---

## K. Recruiting and sales outreach

### K1. LinkedIn Hiring Assistant
- **Deployer / vendor.** LinkedIn, built in-house on LangGraph and its own platform.
- **Dates.** QCon London 2025 talk, published 2025-12-31. LeadDev article 2025-10-31. Hiring Assistant 2 announced 2026-09-29.
- **URLs.**
  - https://infoq.com/presentations/LinkedIn-agent-hiring-assistant
  - https://leaddev.com/ai/how-linkedin-built-ai-hiring-agent
  - https://news.linkedin.com/2026/hiring-assistant-2?linkId=100000441310616
- **Quote.** "Everything we did before, that whole flow chart I was showing earlier, that's all now one skill under one agent."
- **End to end.**
  - A supervisor agent hands work to sub-agents:
    - **intake** turns the recruiter's notes and job description into qualifications;
    - **sourcing** runs many parallel queries against Recruiter Search;
    - **evaluation** uses a fine-tuned model that cites evidence from each profile.
  - Agents talk to each other over LinkedIn's messaging infrastructure: messages in a thread are first-in, first-out, and more threads give parallelism.
  - A skill registry is protected by service principals.
  - Memory is layered: working, episodic, procedural and collective.
  - Applicant tracking systems are connected through APIs.
- **Human in the loop.** The agent mostly recommends and the recruiter takes the action ("still in the driver's seat"). It asks rather than guessing.
- **Scale.**
  - 48% less time reviewing applications, and 62% fewer profiles reviewed.
  - Hiring Assistant 2: more than 20,000 companies, prescreening in a median 6 minutes.
- **Hardest constraints.**
  - Employment-law fairness.
  - Contacting candidates on the recruiter's behalf.
  - Personalising across a billion profiles.
- **Parallel.** Design LinkedIn Recruiter search plus outreach.

### K2. Salesforce Agentforce SDR on Salesforce's own pipeline
- **Deployer / vendor.** Salesforce, on Agentforce.
- **Date.** 2025-10-09.
- **URL.** https://www.salesforce.com/blog/ai-for-lead-qualification/
- **Quote.** "An agent autonomously follows up on every lead and turns them into opportunities."
- **End to end.**
  1. Inbound leads (forms, events, webinars) are assigned to the agent.
  2. It sends a personalised first email and a follow-up sequence.
  3. When someone replies, it judges their interest, sends a meeting link and copies the human rep.
  4. It answers questions from uploaded documentation.
  5. Everything is logged on the lead record.
- **Disclosure.** Every email says it comes from Agentforce.
- **Human oversight ratio.** Planned at 1 SDR to 15,000 leads a month, up from 500.
- **Scale.** 68,000 leads, 156,000 emails, 2,400 replies, 800 meetings booked autonomously, "dozens" of deals.
- **Hardest constraints.**
  - Brand and spam risk at volume.
  - Disclosing that the sender is an AI.
  - Handing off to a human without dropping the thread.
- **Parallel.** Design an email campaign or CRM sequencer where an agent sends.

---

## L. Real estate and property management

### L1. EliseAI at Asset Living: leasing, delinquency and renewals agents
- **Deployer / vendor.** Asset Living (more than 450,000 units, the second-largest property manager on the NMHC Top 50 list), and EliseAI.
- **Date.** 2025-09-16.
- **URL.** https://www.assetliving.com/blogs/asset-living-advances-operational-excellence-with-eliseai-partnership
- **Quote.** "EliseAI helps us automate the routine so our associates can focus on high-impact, human-first resident interactions."
- **End to end.**
  - LeasingAI nurtures leads around the clock.
  - The delinquency agent sends personalised rent reminders.
  - Renewals, maintenance and VoiceAI are deployed but not detailed. AI-guided tours were a pilot.
- **Human in the loop.** Escalation is not described.
- **Scale.**
  - More than 130,000 payment reminders in Q2 2025.
  - On-time rent up 600 basis points; occupancy up 300 basis points.
  - 78.2 hours of capacity added per community per month.
- **Hardest constraints.**
  - Fair-housing law.
  - Collections communications.
  - Coordinating across many properties.
- **Parallel.** Design Airbnb or Zillow Rentals operations with an agent as the leasing office.

(The Aldar service-charge payment, B2, also belongs to real estate. Zillow's ChatGPT app was not fetched; search results say it hands tours and financing back to Zillow.)

---

## M. Healthcare: prior authorisation and clinical trials (reference capability only)

### M1. Claude for Healthcare: a prior-authorisation review skill and clinical-trial connectors
- **Vendor.** Anthropic. No named prior-auth or trial-matching deployment was found.
- **Date.** 2026-01-11.
- **URL.** https://www.anthropic.com/news/healthcare-life-sciences
- **Quote.** The page states "These integrations are private by design." It has no agentic sentence to quote.
- **What exists.**
  - A sample prior-auth skill that pulls coverage rules from the CMS Coverage Database or custom policies, checks clinical criteria against patient records, and proposes a determination with supporting material for the payer to review.
  - Connectors for ICD-10, the NPI registry, Medidata and ClinicalTrials.gov.
  - Skills for trial protocol drafting and enrolment tracking.
- **Status.** This is a template, not a deployment. The search found no Claude or OpenAI payer deployment for prior auth, and no production agentic trial-matching system. That domain is still a gap.

---

## N. Borderline cases: support agents with consequential actions, and delivery by forward-deployed engineers

### N1. SiriusXM "Harmony" (Sierra)
- **URL.** https://sierra.ai/customers/siriusxm (undated, © 2026)
- **Quote.** "Harmony soon aligned to SiriusXM's business requirements and began testing top use cases in production."
- **Why it is here.** Harmony processes payments, updates billing, and refreshes in-car radios, which means sending a signal to the vehicle by satellite. Those are consequential actions on a base of 34 million subscribers.

### N2. OpenAI Presence: voice and chat agents installed by forward-deployed engineers
- **Date.** 2026-07-22.
- **URL.** https://appwrite.io/blog/post/openai-presence-brings-trusted-ai-agents-to-production
- **Quote.** "OpenAI Presence is a proven enterprise product for putting AI agents to work across customer and internal workflows."
- **What it is.**
  - Deployments are led by OpenAI's forward-deployed engineers (FDEs) or systems integrators.
  - Each agent has a scoped job, policies and SOPs, an approved list of actions, guardrails and escalation, and is tested in simulation before launch.
  - In a **Codex improvement loop**, Codex studies production sessions and proposes changes, and the customer approves a controlled rollout.
- **Results.** It resolves 75% of calls on OpenAI's own English phone support. BBVA, SoftBank and IAG are exploring it.
- **Why it is here.** This is the public example of the FDE delivery model in practice.

---

## Count by domain (core entries; references and borderline cases in brackets)

| Domain | Entries | Count |
|---|---|---|
| A. Agentic commerce | A1–A7 [A8 reference] | 7 |
| B. Agent-initiated payments | B1–B3 | 3 |
| C. Travel and mobility | C1–C2 | 2 |
| D. Retail ops, merchandising, marketplace | D1–D3 | 3 |
| E. Procurement and supply chain | E1–E2 (E2 bundles OpenAI/PwC, Ramp and dots) | 2 |
| F. Finance ops (AP, invoicing, payroll) | F1–F4 | 4 |
| G. KYC/AML and fintech risk | G1–G2 | 2 |
| H. Insurance claims and underwriting | H1–H4 | 4 |
| I. Freight and logistics | I1–I3 | 3 |
| J. Legal negotiation and tax | J1–J2 | 2 |
| K. Recruiting and sales outreach | K1–K2 | 2 |
| L. Real estate and property | L1 | 1 |
| M. Healthcare | [M1 reference only] | 0 |
| N. Borderline | [N1–N2] | 0 |
| **Total** | 35 core, plus 1 reference architecture, 1 healthcare reference and 2 borderline | **35** |

---

## Cross-cutting patterns

1. **The irreversible step belongs to whoever owns the liability.**
   - Instant Checkout began with payment inside ChatGPT, then gave checkout back to merchants in March 2026 (A1, A3).
   - Expedia, Booking.com and Uber Eats complete on their own sites (C2, A6). Swiggy allowed cash on delivery only (A5).
   - Design implication: the boundary between platform and merchant is a design choice about who carries chargebacks, loyalty and the customer relationship. It is not an implementation detail.
2. **Agents get credentials scoped to them, not a human's credentials.**
   - Stripe's SPT is limited to one merchant and one basket total.
   - Mastercard issues an Agentic Token to each agent. UPI Reserve Pay earmarks funds for approved merchants.
   - OpenAI's specialist dots get their own organisational identity.
   - Design implication: an agent's identity, its spend scope and the user's mandate are separate objects.
3. **The human signs off on the money and closes the case.**
   - Nemo never automates the payout (H1). FIS will not close an AML case without an analyst (G1). Qonto confirms every financial action (F2). TaxGPT ends in a CPA signature (J2). Amazon Seller Assistant acts only after approval (D2).
   - The fully autonomous counter-examples are Project Deal (A7) and C.H. Robinson's operational agents (I1, I2). In Project Deal the stakes were small and capped. C.H. Robinson's actions can be corrected afterwards.
4. **Specialists under a planner or supervisor is the default shape.**
   - Allianz runs 7 agents, Priceline more than 10, C.H. Robinson more than 30. LinkedIn uses a supervisor with sub-agents. Revionics splits gap detection, impact forecasting and rule enforcement. Brex splits detection, judgment and follow-up.
   - The point is less parallelism than **separate authority**. The agent that decides is not the one that executes or audits.
5. **An audit trail is a product requirement.**
   - DXC logs every action so a regulator can reconstruct the decision. FIS links each statement to its source record. The Allianz and Anthropic partnership is building an audit layer.
   - Design implication: the trace is the compliance artifact, so it must be designed up front.
6. **Legacy interfaces are the real integration surface.**
   - Agents drive the SAP GUI and supplier portals (Duvo), type cards into vendor portals (Ramp), operate tax software in a browser (TaxGPT), browse sites without APIs (Operator), and call carriers by phone (C.H. Robinson, HappyRobot).
   - Design implication: plan for flakiness, idempotency and retries on UIs that were built for humans.
7. **A supervisor agent on the same model adds little.**
   - In Project Vend 2, the CEO agent approved lenient requests about 8 times as often as it denied them. Requiring Claudius to check prices and delivery times did more good.
   - Model asymmetry also matters: in Project Deal, weaker agents got worse deals and their humans did not notice (A7).
   - Design implication: put deterministic checks and independent verification ahead of piling up supervisors.
8. **Route work across models by complexity and stakes.**
   - DXC sends triage to light models and long claim files to frontier models. Qonto routes across Opus, Sonnet and Haiku by task.
   - Design implication: cost and latency budgets belong to each sub-task, not to the whole agent.
9. **Memory of human decisions turns approvals into policy.**
   - Duvo stores each human approval for future runs. LinkedIn's layered memory learns recruiter preferences. Ramp learns GL coding from history.
   - Design implication: the approval log doubles as training data and as precedent, which raises the question of how to stop a one-off exception from becoming the rule.
10. **Delivery by forward-deployed engineers is part of the architecture.**
    - OpenAI Presence, Duvo's eight weeks to production, and OpenAI's "customer zero" finance work all depend on embedding engineers to write SOPs, approved action lists and evals for each customer.
    - Design implication: per-tenant policy configuration and an improvement loop (here, Codex proposing changes and humans approving them) are first-class components.

---

## Protocols that create new design problems

| Protocol / development | Date | What it adds | Design problem it creates | Verified link |
|---|---|---|---|---|
| **Agentic Commerce Protocol (ACP)**, OpenAI and Stripe | 2025-09-29; extended to discovery 2026-03 | Merchant checkout over REST or MCP. Stripe Shared Payment Token scoped to merchant and basket. Merchant stays merchant of record. | Delegated payment credential. Who owns checkout. Agent-ready product feeds. | https://www.agenticcommerce.dev/ and https://stripe.com/newsroom/news/stripe-openai-instant-checkout |
| **Agent Payments Protocol (AP2)**, Google | 2025-09-17 | Signed Intent and Cart mandates (verifiable credentials). Human-present and human-absent modes. x402 extension for stablecoins. More than 60 partners. | A chain of mandates that cannot be repudiated. Autonomous purchases triggered by conditions. Dispute evidence. | https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol |
| **Universal Commerce Protocol (UCP)**, Google with Shopify, Walmart, Target, Etsy and Wayfair | 2026-01-11 | Primitives for checkout, identity linking and order management over REST, MCP or A2A. Compatible with AP2. Merchant stays merchant of record. | Account linking and loyalty across agent surfaces. Competes with ACP, so merchants must support both. | https://developers.googleblog.com/en/under-the-hood-universal-commerce-protocol-ucp/ |
| **MCP Apps** (SEP-1865), the first official MCP extension | 2026-01-26 | Tools return interactive UI in a sandboxed iframe. JSON-RPC over postMessage. Hosts may require approval for tool calls the UI starts. | Generative UI as an attack surface. Consent for actions the UI triggers. Rendering across hosts. | https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/ |
| **Agent2Agent (A2A)**, Google with more than 50 partners | 2025-04-09 | Agent Cards for capability discovery. A task lifecycle with artifacts. Long-running tasks with humans in the loop. | Delegating across organisations to opaque agents. Trust and authentication between agents. | https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ |
| **Visa Trusted Agent Protocol (TAP)** and Intelligent Commerce | 2025-10-14; live in Europe 2026-07-02 | Agent identity via HTTP Message Signatures (Web Bot Auth), built with Cloudflare. Passkey-authenticated agent transactions. | Telling legitimate agents from bots at the merchant edge. Strong Customer Authentication for agents. | https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html |
| **Mastercard Agent Pay** | First live APAC transactions 2026-03 | An Agentic Token issued to each agent, Payment Passkeys, explicit consent. | Credentials scoped to an agent. Revoking them. Recording what the cardholder authorised. | https://www.artificialintelligence-news.com/news/mastercard-agentic-payments-singapore-dbs-uob/ |
| **x402** (HTTP 402 payments) | Page updated 2026-08-25 | Pay-per-request over HTTP, mostly in stablecoins. The page shows about 75M transactions and $24M volume over 30 days. | Micropayments by agents for APIs and data. Budgets per run. Checking that receipts are real. | https://www.x402.org/ ; reference flow with approvals at https://developers.openai.com/cookbook/examples/partners/aws/controlled_agentic_commerce_with_agentcore_payments/controlled_agentic_commerce |
| **UPI Reserve Pay and UPI Circle** inside ChatGPT, NPCI | 2025-10-09 | Pre-authorised funds earmarked for merchants, and delegated authentication on a real-time rail. | Mandates on a rail that cannot be reversed. National-scale rate limiting. | https://techcrunch.com/2025/10/09/india-pilots-ai-chatbot-led-e-commerce-with-chatgpt-gemini-claude-in-the-mix |
| **Agent identity at the enterprise level**: OpenAI specialist dots and Microsoft Agent 365 | 2026-10-02 | Agents get their own organisational identity, credentials and approval processes, governed by the enterprise. | The agent as a non-human employee: provisioning, least privilege, removing access, audit. | https://itbrief.co.uk/story/openai-launches-dots-always-on-ai-agents-for-work |

---

## Couldn't verify, and gaps

- **openai.com pages returned 403**, and I did not get around the block. These were not read directly: buy-it-in-chatgpt, introducing-operator, introducing-dots, openai-pwc-finance-collaboration, openai-contract-data-agent, instacart-partnership, basis, introducing-agentkit, introducing-openai-presence. Each one is covered through a partner page or trade press. OpenAI's own Basis case study (accounting agents on GPT-5) was **not included** because no non-OpenAI page confirming it was fetched.
- **No public write-ups from OpenAI's forward-deployed engineering team** beyond Presence. Searching only turned up job postings.
- **No named prior-authorisation or clinical-trial-matching deployment** on Claude or OpenAI. Section M is a reference capability only.
- **No LLM-agent loan-underwriting deployment** at a named bank (Rocket's figures are mostly document processing from 2023–2024). AIG (H4) is insurance underwriting, and Brex (G2) gives little detail.
- **Palantir AIP** (AIG's multi-agent underwriting and claims, Heineken's supply chain) and **Scale AI** cases appear only in secondary or earnings-call summaries. Not included.
- **Unilever's multi-agent procurement on Google's Agent Platform** (Next '26) and **GE Appliances' 800 agents**: only secondary coverage, and nothing was fetched. Not included.
- **No LinkedIn Pulse or LinkedIn posts with real architecture detail turned up.** LinkedIn's own engineering post on Hiring Assistant returned HTTP 400, so InfoQ and LeadDev stand in for it.
- **The DoorDash and Uber agentic-ordering test in Gemini** (Retail TouchPoints) returned 403. Not included.
- **Some dates are only implied.** Brex's year, and the DXC, Duvo, Qonto and SiriusXM pages, show no date (© 2026 only). Luminance's own page reported an implausible "today" publish date, so the IT Brief date was used.
- Nothing in this sweep parallels a parking-lot design problem, and nothing parallels Splitwise directly. Intuit's invoicing and reminders agent (F3) is the closest.

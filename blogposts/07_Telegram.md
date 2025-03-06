# Deploying Telegram bots on Ratio1: from Echo-bot to Blackjack-dealer

**Looking for a way to run Telegram bots that combine decentralized infrastructure with robust AI capabilities?** You’re in the right place. In this introductory post, we’ll show you how to deploy two Python-based Telegram bots on the **Ratio1** network: a straightforward Echo Bot and an interactive Blackjack Bot. Although neither bot is particularly complex nor do they use AI models, they serve as a solid foundation for understanding how to leverage Ratio1’s decentralized environment for your own projects. In the later posts we are going to explore deploying various agents as Telegram bots on Ratio1.
By the end, you’ll see how easily Ratio1’s infrastructure handles everything from basic message responses to more complex, stateful game logic—all with minimal setup.

---

## Why Telegram bots on Ratio1?

### 1. Decentralized & Trustless
In Ratio1, each bot runs in a **decentralized** environment, secured by the **dAuth** systemm using ChainStore real-time key-value distributed-decentralized in-memory database and R1 IPFS API for blob storage. Instead of hosting your bot on a single centralized server, you leverage a global network of Edge Nodes. This eliminates single points of failure and ensures your bot remains resilient.

### 2. Scalable & Secure
Bots can scale horizontally across multiple Edge Nodes, and data is managed securely using cryptographic keys. This approach is especially appealing if you expect a surge in traffic or require strong data ownership guarantees—important for both developers and investors.

### 3. Minimal Overhead
Forget about spinning up separate VMs or messing with complex DevOps pipelines. With Ratio1, you **define your logic** and **deploy**—that’s it. The integrated system automatically takes care of containerization, routing, and authentication.

>**TL;DR:** You own the data, you own the code, costs and deployment. Your system secured by Blockchain.

---

## Prerequisites

1. **Running Edge Node**  
   You’ll need a **Ratio1 Edge Node** up and running. For testing, this can be on your local machine or a remote server. You can find instructions in our other tutorials on how to spin up a node with Docker so please refer to our specific posts and tutorials for more details on how to spin up a Ratio1 Edge Node both for the **free** faucet-based Testnet as well as for the Mainnet where on-chain (Base L2) Node Deed licensing is required.

2. **Python & Ratio1 SDK**  
   Ensure you have Python 3+ installed along with the Ratio1 SDK (`ratio1`).  
   
   ```bash
   pip install ratio1 --upgrade
   ```
   > **Note**: The `ratio1` will soon be migrated to `ratio1` package name.

3. **Telegram Bot Token**  
   Generate a Bot Token using @BotFather [BotFather](https://core.telegram.org/bots#6-botfather) on Telegram. You’ll insert this token into the code shortly.

---

## Part 1: The Echo Bot

### Code Walkthrough

Below is a basic Echo Bot designed to reply to user messages with a playful twist—tracking each user’s message count:

```python
# epoch.py

import os
import time

from ratio1 import Session, CustomPluginTemplate, PLUGIN_TYPES

def reply(plugin: CustomPluginTemplate, message: str, user: str):
  """
  This function is used to reply to a message. The given parameters are mandatory
  """
  # Each user message increments a counter
  plugin.int_cache[user] += 1
  plugin.P(f"Replying to the {plugin.int_cache[user]} msg of '{user}' on message '{message}'")
  result = f"The answer to your {plugin.int_cache[user]} question is in the question itself: {message}"
  return result

if __name__ == "__main__":
  my_node = os.getenv("EE_TARGET_NODE", "0xai_my_own_node_address")
  
  session = Session()
  session.wait_for_node(my_node)

  # Create a Telegram bot pipeline
  pipeline, _ = session.create_telegram_simple_bot(
    node=my_node,
    name="telegram_bot_echo",
    telegram_bot_token="your_token_goes_here",  # Insert your actual token
    message_handler=reply,
  )

  # Deploy it on your chosen Edge Node
  pipeline.deploy()

  # Keep the pipeline alive for two minutes, then clean up
  session.wait(
    seconds=120,
    close_pipelines=True,
    close_session=True,
  )
```

#### Key Points

- **`reply(plugin, message, user)`**: Your custom callback function that defines how the bot responds.
- **`plugin.int_cache[user]`**: A plugin system built-in integer cache for persisting data between user messages. Sufficient for counting messages, storing small preferences, etc.
- **`session.create_telegram_simple_bot(...)`**: This makes it easy to bring up a Telegram bot pipeline with a single method call, passing in your Telegram token.

Once you run `python epoch.py`, your Echo Bot will be online, echoing messages from any user who starts a conversation with it on Telegram.

---

## Part 2: The Blackjack Bot

### Code Walkthrough

Want to create something more interactive? **Blackjack Bot** showcases how to handle game logic (e.g., deck states, user hand values) within Ratio1’s decentralized environment.

```python
# blackjack.py

import os
import time

from ratio1 import Session, CustomPluginTemplate

def reply(plugin, message: str, user: str):
  cards = ['2', '3', '4', '5', '6', '7', '8', '9',
           '10', 'Jack', 'Queen', 'King', 'Ace']
  card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10,
    'Jack': 10, 'Queen': 10, 'King': 10,
    'Ace': 11  # Initially 11; adjusted if needed
  }

  # Initialize user game state if not present
  if user not in plugin.obj_cache or plugin.obj_cache[user] is None:
    plugin.obj_cache[user] = {
      'state': 'NOT_STARTED',
      'wins': 0,
      'losses': 0
    }

  user_cache = plugin.obj_cache[user]
  message = message.strip().lower()

  # Handle game states
  # ...
  # The code orchestrates dealing cards, evaluating aces, handling hits/stops,
  # and updating wins/losses. See the full snippet for logic details.
  # ...

  return "Some relevant response based on the current Blackjack logic."

  ## NOTE: The full code is available in the Ratio1 SDK examples
  ##       https://github.com/ratio1/ratio1_sdk/blob/main/tutorials/ex11_telegram_blackjack_bot.py

if __name__ == "__main__":
  my_node = os.getenv("EE_TARGET_NODE", "0xai_your_node_address")
  
  session = Session()
  session.wait_for_node(my_node)

  pipeline, _ = session.create_telegram_simple_bot(
    node=my_node,
    name="telegram_bot_blackjack",
    message_handler=reply,
  )

  pipeline.deploy()
```

#### Key points

- **Stateful Experience**  
  The `plugin.obj_cache[user]` dictionary lets you store more complex objects—like card hands and win/loss counts—between messages. Through the `plugin` object, you can access the whole plethora of business processing templates, advanced data management, and even shallow machine learning features Ratio1 offers (as the Deep Learning models are served by a different layer that feeds the data to the business plugins layer).

- **Card Logic & Deck Management**  
  Demonstrates how you can integrate real-time calculations (like adjusting Ace from 11 to 1) without losing state across multiple user interactions.  

- **Zero DevOps Overhead**  
  You focus on the game logic; Ratio1 handles the decentralized environment, ensuring high availability and security.

---

## HowiIt works under the hood

### 1. Pipelines & Plugins
Ratio1 leverages a concept of **pipelines** for running services, and **plugins** to house both pre-made templates as well as your custom code. When you call `create_telegram_simple_bot`, you’re effectively spinning up a new pipeline with the embedded plugin instance for Telegram bot with all required dependencies (i.e. a Telegram interface plus your callback function).

### 2. Edge Node deployment
Your bot lives on a selected **Edge Node**, which acts as the compute layer. Because it’s decentralized, you can choose one or multiple nodes across different geographical regions—or even in your own data center. In our case we deploy on the local node. Note that the SDK connects to the local node as on any other node no matter the location/distance.

### 3. dAuth 
Ratio1’s **dAuth** system ensures that any pipeline or plugin creation and deployment process is authenticated trustlessly. No single authority has ultimate control over your data, which is especially appealing to investors and teams that prioritize data sovereignty. Data democracy is the name of the game!

---

## Common use cases

- **Community Engagement**: Quickly set up fun or utility bots—like polls, games, or daily tips—directly in Telegram without the usual infrastructure overhead.
- **Customer Service**: Offer decentralized support channels that can automatically handle load balancing, ensuring consistent performance.
- **Gamification & Loyalty**: Build on-chain reward systems or tournaments that store player progress and results across multiple channels.

---

## Conclusion & next steps

Deploying Telegram bots on Ratio1 is a **powerful, streamlined experience** that merges decentralized infrastructure, robust security, and minimal overhead. Whether you’re spinning up a simple Echo Bot or a stateful Blackjack Bot, Ratio1’s plugin system ensures your code can scale—and remain fault-tolerant—across a global network of Edge Nodes.

**Ready to take it further?**  
- Integrate advanced AI or GPT-based models to handle more nuanced conversation flows or specialized tasks.  
- Connect your bot to external APIs, payment systems, or on-chain data.  
- Explore multiple node deployments for enhanced redundancy and performance.

**Ratio1** opens the door to a new era of bot deployment where data ownership, security, and ease-of-use are front and center. Let your creativity run wild, and watch your Telegram bots come to life in a truly next-generation environment!

---

*Stay tuned for more tutorials, tips, and advanced examples as we continue exploring the infinite possibilities of decentralized AI applications on the Ratio1 network.*


<h1 align="center">
📖 ft_blockchain - 42 Cibersecurity
</h1>

<p align="center">
	<b><i>Blockchain what its</i></b><br>
</p>

<p align="center">
	<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/Falitomal/ft_blockchain?color=lightblue" />
	<img alt="Code language count" src="https://img.shields.io/github/languages/count/Falitomal/ft_blockchain?color=yellow" />
	<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/Falitomal/ft_blockchain?color=blue" />
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Falitomal/ft_blockchain?color=green" />
</p>



## ✏️ Summary
```

Use any programming language. You can use cryptographic libraries like openssl or hashlib for generating hashes, but the blockchain structure must be implemented by you. In the same way, web frameworks like NestJS or Flask can be used for the server implementation.

```
## 💡 About the project

```
The workflow is to add different transactions to the current block and mine the block so that the string is added.
The proof-of-work or PoW algorithm must be simple, for example, to find the number that, concatenated with the PoW on the previous block, results in a SHA-256 hash ending in 4242. The blockchain will not be persistent, it will be stored in the server's memory but the server will not be connected to any specific database software.
```
## 🛠️ Mandatory
```
When developing mining, three things must be done:
- Calculate the proof of work
- Rewarding the miners (a transaction)
- Create the new block and add it to the chain.
Once the blockchain is created, it will be possible to interact with it through different HTTP requests:
- [POST] /transactions/new : Sends a new transaction to add to the next block.
- GET] /mine : Executes the proof of work and creates a new block.
- GET] /chain : Returns information about the blockchain (blocks, tran- sactions, etc).

```
##  Bonus
```
The evaluation of the bonuses will be done IF AND ONLY IF the mandatory part is PERFECT. Otherwise, the bonuses will be totally IGNORED.
You can improve your project with the following features:
- Dynamic PoW algorithm difficulty, ascending depending on the number of mined blocks or elapsed time.
- Implementation of automated communication with other nodes in the network using a decentralized network and a consensus algorithm to verify the correct chain.
- Implementation of Proof of Stake as an alternative form of consensus (and much more environmentally friendly than PoW).

```
## 🛠️ Usage
```
```
Then in a browser to the IP address of the program send:

POST	

/transactions/new

Sends a new transaction to add to the next block.

/connect_node
Connect differents nodes of chain


GET

/mine	
Executes the proof of work and creates a new block.

/chain
Returns information about the blockchain (blocks, transactions...).

/replace_chain
Check if the chain is the most long chain(correct chain)

```

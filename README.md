## Pet Society Server Emulator

<img width="703" height="70" alt="663" src="https://github.com/user-attachments/assets/21c68e5a-e5b4-497f-bfbc-3c8f475b925a" />


### What is Pet Society?
*Pet Society was a social-network game developed by Playfish that could be played on Facebook. [...] Players could design their pets by choosing genders, names, colors and altering appearances. The user interacted with their pets through washing, brushing, petting and feeding.*

[Source](https://en.wikipedia.org/wiki/Pet_Society)

### Why?
Pet Society is a game that deserves to be preserved. This project is inspired by the original Nofil2000 server emulator, a lot of the already implemented features helped inmensely in the development of this emulator. It is also inspired by the amazing project by [AcidCaos](https://github.com/AcidCaos), [Raise the Empires](https://github.com/AcidCaos/raisetheempires). Go check that project too!

### How to run
#### Windows
Windows binaries are provided in the [releases page](https://github.com/DexterX12/mascotsociety/releases/). After extracting the files, you should see both `play.exe` and `profile.pet` files. Just open `play.exe` and the server should start right up.

Finally, go to `http://localhost:8881/` and start playing!

##### Saves
If you want to change the save file, delete or move the `profile.pet` file and put your own file, its extension can be either `.pet` or `.nofil`, just remember to name your save file as `profile`.

####
#### macOS
macOS binaries are provided for the latest release in the [releases page](https://github.com/DexterX12/mascotsociety/releases/). After extracting the files, you should see both `play` and `profile.pet` files. Open a terminal inside the folder where these 2 files reside an execute the command `./play`, this will execute the server in the same directory where the save file is located.

#### Saves
They are managed the same way as on Windows.

#### Linux
Make sure you have at least Python 3.11 installed.
1. Clone this repository or download it and extract it. Then go inside the root directory.
2. Open a terminal inside the directory
3. Create a Python virtual environment like this:
	```bash
	python -m venv .venv
	```
4. Install Flask
	```bash
	python -m pip install flask
	```
5. Since this project uses relatives imports, the server has to be initialized as a module from its parent directory. Go to the server's parent directory and then execute this command:
	```bash
	python -m foldername.app
	```
	where foldername is the directory name where the server is located. If you cloned this repo, the name should be mascotsociety
6. Go to `http://localhost:8881/` and start playing.

Everytime you need to open the server, the virtual environment has to be activated. With your terminal inside the game's root directory, execute this command:
```bash
source ./venv/bin/activate
```
then you can go through steps 5-6.
##### Saves
For loading your save file, make sure its named "profile" and it is inside the server's directory.


### How does it work?
Pet Society and similar Playfish games use a custom binary RPC protocol, with different messages types and possible "batch" operations. The game uses big-endian or byte network order when exchanging data, but some byte reading/write operations are protocol specific.

The key in the emulator is to be able to mimic the custom RPC protocol that  the game's ActionScript 3 client expects.

More info about how a similar game works can be found [here](https://nettech.fandom.com/wiki/SimCity_Social)

##### Disclaimer
Most code regarding the communication and byte order was written AI assisted, since my knowledge in AS3 is very little, and the decompiled AS3 client code is obfuscated in those parts, too.

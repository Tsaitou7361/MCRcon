# Minecraft Remote Console
* MCRcon is a function provided by Mojang. You can open it in `server.properties`

## Before Starting
* Open Rcon service in `server.properties`
```properties
# ...
enable-rcon=true
# ...
rcon-password=set-your-password-here
rcon-port=25575
# ...
```
> [!IMPORTANT]
> Default Rcon password is 25575, DO NOT USE as same as SERVER PORT!
>
> Because if your password known by others, your server might not be safe!

> [!CAUTION]
> We strongly recommend using Rcon in the Intranet instead of external network.


## Starting
* Config file is in `%localappdata%\Programs\mcrcon-win-2.0\config.yml`
* Login with server ip and rcon password, and then press connect.
> [!TIP]
> You can also press connect with Enter

* After login, you will be taken to Console, you can type in any command into the console.
> [!TIP]
> You can exit the console by `exit` command.
> 
> You can also send the command with Enter.

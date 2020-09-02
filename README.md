# Docker Registry UI

##Usage

It does not need to be connected with the docker sock. You can easly log in a registry with Your **User** **Password** and **REGISTRY_URL:PORT**. To connect another registry, all you need is logging out of the registry you are connected to and log in again with the new one. It only works with **basic auth** and docker registry **v2**.

As an example, you can run it as follows.

docker run -p 5003:5001 chosenwar/registryui:latest


![](registryuiapp.gif)

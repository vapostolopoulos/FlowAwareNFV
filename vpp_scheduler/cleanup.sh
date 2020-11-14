ps -ef | grep vpp | awk '{print $2}'| xargs sudo kill
sudo rm -rf /run/vpp/cli-*
sudo rm -rf /run/vpp/stats-*
sudo rm -rf /run/vpp/vpp*
sudo rm /run/vpp/memif{1..17}.sock

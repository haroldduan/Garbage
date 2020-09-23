#!/usr/bin/env bash

{ # this ensures the entire script is downloaded #

echo \ '
###################################################################
# giprote                                                         #
# Gitea project template kits.                                    #
# AVATech-RDC support                                             #
# Copyright AVATech-RDC@2020                                      #
###################################################################
'
cur_path=$PWD
echo $cur_path
echo "Downloading..."
# cd $USERPROFILE
# cd $HOME
rm -rf $HOME/.giprote
mkdir $HOME/.giprote
#sudo chown ${USER} $giprote_dir
#sudo chmod -R 777 $giprote_dir
# export giprote_dir=$HOME/.giprote
# if ! grep -q "$HOME/.giprote/" $HOME/.bashrc; then cat>>$HOME/.bashrc<<EOF
# export PATH=$PATH:$HOME/.giprote/
# EOF
# fi
# grep -q "$HOME/.giprote/" $HOME/.bashrc || echo "export giprote_dir=$HOME/.giprote" >> $HOME/.bashrc
export PATH=$PATH:$HOME/.giprote/giprote.commandline
export giprote_dir=$HOME/.giprote/giprote.commandline
sudo grep -q "$HOME/.giprote/giprote.commandline" $HOME/.bashrc || sudo cat>>$HOME/.bashrc<<EOF
export PATH=$PATH:$HOME/.giprote/giprote.commandline
export giprote_dir=$HOME/.giprote/giprote.commandline
EOF
# source $HOME/.bashrc
# . $HOME/.bashrc
cd $HOME/.giprote
sudo rm -rf giprote.commandline
git clone https://github.com/haroldduan/giprote.commandline.git
# sudo cp -r $(cd $(dirname $0); pwd -P)/giprote.sh $HOME/.giprote
# sudo -c wget http://rds.avatech.com.cn:7070/harold.duan/giprote.commandline/releases/download/v1.0.1/gpt_v1.2.2.zip
# sudo unzip -o gpt_v1.2.2.zip
echo "Installing..."
cd $giprote_dir
# git branch -r | grep -E "[0-9].[0-9].[0-9]" | while read remote; do git branch --track "${remote#origin/}" "$remote"; done
remotes=$(git branch -r | grep -v "\->" | grep -E "[0-9].[0-9].[0-9]")
# echo $remotes
for remote in $remotes
do
  # echo "$remote"
  git branch --track "${remote#origin/}" "$remote"
  max="0.0.0"
  temp="${remote#origin/}"
  # echo "$temp"
  if [ $temp \> $max ];then
    max=$temp
    # echo "$max"
  fi
done
git checkout $max
git fetch --all
git pull --all
#sudo chown ${USER} $giprote_dir/giprote.sh
#sudo chmod -R 755 $giprote_dir/giprote.sh
#sudo chown ${USER} $giprote_dir/gpt
#sudo chmod -R 755 $giprote_dir/gpt
#cd $cur_path
echo "Done!"
sh $giprote_dir/scripts/copyright.sh "copyright"
while read line; do echo $line; done < $giprote_dir/scripts/version
sh $giprote_dir/scripts/copyright.sh "giprote"
cd $cur_path

} # this ensures the entire script is downloaded #
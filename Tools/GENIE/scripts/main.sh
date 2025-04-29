#!/bin/bash

SCRIPTS='scripts/'

SCRIPT_V=$SCRIPTS'variables.sh'
SCRIPT_S=$SCRIPTS'setup.sh'
SCRIPT_D=$SCRIPTS'delete.sh'
SCRIPT_R=$SCRIPTS'registry.sh'
SCRIPT_U=$SCRIPTS'unzipped.sh'

source $SCRIPT_V

# Operation to work on the full NPM Repository or unzipped packages
OPTION=$@

if [ ! -z "$OPTION" ]; then
    # 检查命令行选项
    if [[ "$OPTION" == *"-u"* ]] || [[ "$OPTION" == *"-b"* ]]; then
        source $SCRIPT_U
    else
        source $SCRIPT_R
    fi
    exit;
fi


PROGRAM_NAME='GENIE'
PS3="$PROGRAM_NAME > "

echo "GENIE | 选择一个操作..."
select action in '帮助' '退出' '初始化' '删除' '分析已解压包'; do
    case $action in
        帮助   ) REPLY='';;
        退出   ) echo "再见!"; exit 0;;
        初始化  ) source $SCRIPT_S; PS3="$PROGRAM_NAME > ";;
        删除 ) source $SCRIPT_D; PS3="$PROGRAM_NAME > ";;
        '分析已解压包' ) source $SCRIPT_U; PS3="$PROGRAM_NAME > ";;
        *      ) echo "未知操作 > $REPLY";;
    esac
done

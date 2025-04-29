
<<doc
Create a CodeQL's DB from @CB_Path, and store it in @DB_Path.
Use @LOG_Path for logging.
doc
UTILS_Create_DB()
{
    CB_Path=$1
    DB_Path=$2
    LOG_Path=$3
    option_BUILDER=${4:-javascript}
    option_VERBOSE=${5:-errors}
    option_THREADS=${6:-1}

    # 使用绝对路径的codeql命令
    CODEQL_PATH="/home/wenbo/NPMAnalysis/Tools/GENIE/codeql/codeql"

    # Limit the RAM to 8GB
    $CODEQL_PATH database create --source-root=$CB_Path      \
                           --language=$option_BUILDER  \
                           --verbosity=$option_VERBOSE \
                           --threads=$option_THREADS   \
                           --ram=8000                  \
                           -J=-Xmx8G                   \
                           $DB_Path &>> $LOG_Path
                           
    # 完成数据库初始化
    $CODEQL_PATH database finalize $DB_Path &>> $LOG_Path
}


<<doc
Compact a CodeQL's DB from @DB_Path, making it as small as possible on disk.
Use @LOG_Path for logging.
doc
UTILS_Clean_DB()
{
    DB_Path=$1
    LOG_Path=$2
    option_VERBOSE=${3:-errors}
    option_CLEANUP=${4:-brutal}

    # 使用绝对路径的codeql命令
    CODEQL_PATH="/home/wenbo/NPMAnalysis/Tools/GENIE/codeql/codeql"

    $CODEQL_PATH database cleanup --verbosity=$option_VERBOSE \
                            --mode=$option_CLEANUP      \
                            $DB_Path &>> $LOG_Path

    exitCODE=$?

    # Delete all CodeQL's log files
    CodeQL_LOG_Path=$DB_Path/log/
    if [ -d $CodeQL_LOG_Path ]; then rm -rf $CodeQL_LOG_Path; fi

    # Delete all CodeQL's binary-result files
    CodeQL_OUT_Path=$DB_Path/results/
    if [ -d $CodeQL_OUT_Path ]; then rm -rf $CodeQL_OUT_Path; fi

    return $exitCODE;
}


<<doc
Apply queries from @QL_Path to a CodeQL's DB from @DB_Path, and store the
results in @OUT_Path. Use @LOG_Path for logging.
doc
UTILS_Query_DB()
{
    QL_Path=$1
    DB_Path=$2
    OUT_Path=$3
    LOG_Path=$4
    option_FORMATS=${5:-csv}
    option_VERBOSE=${6:-errors}
    option_THREADS=${7:-0}
    option_TIMEOUT=${8:-300}

    # 使用绝对路径的codeql命令
    CODEQL_PATH="/home/wenbo/NPMAnalysis/Tools/GENIE/codeql/codeql"
    
    # 确保数据库已完成初始化
    $CODEQL_PATH database finalize $DB_Path &>> $LOG_Path

    # Limit the RAM to 16GB
    $CODEQL_PATH database analyze --rerun                     \
                            --output=$OUT_Path          \
                            --format=$option_FORMATS    \
                            --verbosity=$option_VERBOSE \
                            --threads=$option_THREADS   \
                            --timeout=$option_TIMEOUT   \
                            --no-save-cache             \
                            --ram=16000                 \
                            -J=-Xmx16G                  \
                            $DB_Path                    \
                            $QL_Path &>> $LOG_Path

    exitCODE_Query=$?

    UTILS_Clean_DB $DB_Path $LOG_Path

    exitCODE_Clean=$?

    if [ $exitCODE_Query -ne 0 ]; then
        return $exitCODE_Query;
    else
        return $exitCODE_Clean;
    fi
}


export -f UTILS_Create_DB UTILS_Clean_DB UTILS_Query_DB

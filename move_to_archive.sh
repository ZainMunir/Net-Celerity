if [[ -z $1 ]];
then 
    echo "Please give a name as an arguments"
    exit 1
fi

dir_name=$1

mkdir -p Archive/$dir_name

mv Data/* Archive/$dir_name/
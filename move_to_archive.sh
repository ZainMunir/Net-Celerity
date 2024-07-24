if [[ -z $1 ]];
then 
    echo "Please give a name as an arguments"
    exit 1
fi

dir_name=$1

mkdir Archive/$dir_name
mkdir Archive/$dir_name/logs
mkdir Archive/$dir_name/plots
mkdir Archive/$dir_name/results

mv system_logs/* Archive/$dir_name/
mv logs/* Archive/$dir_name/logs/
mv plots/* Archive/$dir_name/plots/
mv results/* Archive/$dir_name/results/

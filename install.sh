sudo apt-get install gcc g++ gfortran git patch wget pkg-config liblapack-dev libmetis-dev
./coinbrew fetch Ipopt --no-prompt
./coinbrew build Ipopt --prefix=./ --test --no-prompt --verbosity=3
./coinbrew install Ipopt --no-prompt

#include "TrafficModel.h"
#include <iostream>

TrafficModel::TrafficModel() { }
TrafficModel::~TrafficModel(){

  Car* currentCar;
  Car* next;

  int counter = 0;
  int cars = 0;
  
  //Iterates over each platoon
  for (unsigned int i = 0; i < platoons.size(); i++){
    cars = platoons[i].get_size();
    currentCar = platoons[i].get_head();
    counter = 0;
    //Removes each car from a platoon
    while (counter < cars) {
     next = currentCar->get_next();
     delete currentCar;
     currentCar = next;
     counter++;
    }
 }
  currentCar = NULL;
  next = NULL;
}

void TrafficModel::set_commands(vector<string> commands)
{
	this->commands = commands;
}

/* A helper function. 
 * Given a specific id as the input, it searches the lane change command stored in
 * "commands". Returns the value of the turn-light in the command for this car id.
 * 0 = no light, 1 = left light, 2 = right light.
 */
int TrafficModel::get_lane_change_command(int id)
{
	int count = commands.size();
	for (int i = 0; i < count; i++){
		size_t found = commands[i].find(',');
		string iter_id = commands[i].substr(0, found);
		string light = commands[i].substr(found+1, commands[i].size()-1);
		stringstream ss1(iter_id);
		int id_value;
		ss1 >> id_value;
		if (id_value == id){
			stringstream ss2(light);
			int light_value;
			ss2 >> light_value;
			return light_value;
		}
	}
	return 0;
}

/*
 * The function that updates the vehicle positions and states.
 */
void TrafficModel::update()
{
  Car* currentCar;
  int coefficient = 0;
  int indicator = 0;

  //This vector will store any vehicles that have been moved during this tick, so they cannot perform multiple actions
  vector<Car*> moved;
  bool retrievedNext = false;
  
  //Iterates through the platoons
  for (unsigned int i = 0; i < platoons.size(); i++){
    //Start with the car at the highest position
    currentCar = platoons[i].get_head();

    //Iterates through all cars within a platoon
    while(currentCar != NULL){
      //Will only do something if the car hasn't been moved this tick
      if(!alreadyMoved(currentCar,moved)){
        //Gets indicator and determines action based on the output.
        //If there is an indicaor, coefficient stores if the lane is above or below the current platoon
        indicator = get_lane_change_command(currentCar->get_id());
        if(indicator == 1){
          coefficient = -1;
        }
        else if(indicator ==2){
          coefficient = 1;
        }

        if(indicator == 0){
          //Check there will not be a collision from the movement. If there will be, it does not move
          if(validMove(currentCar, i)){
            currentCar->set_position(currentCar->get_position() + 1);
            moved.push_back(currentCar);
          }
        }
        // Runs if there is an indicator turned on
        else{
          //Edge cases for indicators, or if the lane change will cause a collision
          if((i == 0 && indicator == 1) || (i == platoons.size() && indicator == 2)|| !validLaneChange(currentCar->get_position(), i, coefficient)){
            //If it cannot change lanes, only move forward if it will not result in a collision
            if(validMove(currentCar, i)){
              currentCar->set_position(currentCar->get_position() + 1);
              moved.push_back(currentCar);
            }
          }
          else if(!alreadyMoved(currentCar, moved)){
            //If there is another behind the current car in lane, we should remember this car and deal with it next
            if(currentCar != platoons[i].get_tail()){
              Car* temp = currentCar->get_next();
              platoons[i].remove(currentCar);
              platoons[i+coefficient].insert(currentCar);
              moved.push_back(currentCar);
              currentCar = temp;
              retrievedNext = true;
            }
            else{
              //If there are no other cars in the lane, we don't need to remember the next car in lane
              platoons[i].remove(currentCar);
              platoons[i+coefficient].insert(currentCar);
              moved.push_back(currentCar);
            }
          }
        }
      }
    //If we have already fetched the next car from the lane change case, then we don't need to get the next car
    if(!retrievedNext){
      currentCar = currentCar->get_next();
    }
    //Reset the boolean at the end of the loop
    retrievedNext = false;
    }
  }
}

//Determines whether or not a car can switch lanes
bool TrafficModel::validLaneChange(int pos,int lane, int indicator){

  Car* currentCar = platoons[lane+indicator].get_head();
  //Iterates throug the cars in that lane and returns false if there is a car in the position it wants to merge into, otherwise it will return true
  while(currentCar != NULL){
    if(currentCar->get_position() == pos){
      return false;
    }
    currentCar = currentCar->get_next();  
  }
  return true;
}

/* Determines whether or not a car has already moved in this tick by matching ID numbers to all the cars that have already moved */
bool TrafficModel::alreadyMoved(Car* c, vector<Car*> laneChanged){
  for(unsigned int i = 0; i < laneChanged.size(); i++){
    //Searches for a car that's already moved with the same ID, if it finds one, then it immediately returns true
    if(c->get_id() == laneChanged[i]->get_id()){
      return true;
    }
  }
  return false;
}

/*Checks if the car can move into that position in lane or if there will be a collision */
bool TrafficModel::validMove(Car* c, int lane){
  Car* currentCar = platoons[lane].get_head();

  //Iterate through the linked list. 
  while(currentCar != NULL){
    //Checks if there is a car in the position we are intending to move into
    if(currentCar->get_position() == c->get_position() + 1){
      return false;
    }
    currentCar = currentCar->get_next();
  }
  return true;
}


/*
 * Initialization based on the input information
 */
void TrafficModel::initialize(vector<string> info)
{
	int lane_count = info.size();
	for (int i = 0; i < lane_count; i++){
		Platoon p = Platoon(info[i]);
		platoons.push_back(p);
	}
}

//
// IMPORTANT: DO NOT CHANGE THE FUNCTIONS BELOW THIS LINE
//

// Returns all the vehicle states in the system
vector<string> TrafficModel::get_system_state()
{
	vector<string> output;
	int size = platoons.size();
	for (int i = 0; i < size; i++){
		// get the last vehicle in the platoon
		Car* temp = platoons[i].get_tail();
		string s = "";
		ostringstream out;
		while (temp != NULL){
			out << ";(" << temp->get_id() << "," << i << "," << temp->get_position() << \
					 "," << get_lane_change_command(temp->get_id()) << ")";
			temp = temp->get_prev();
		}

		output.push_back(out.str());
	}
	return output;
}

//Get the state of cars as a 3D vector representing car data in lane/pos
vector<vector<vector<int>>> TrafficModel::get_car_state(){

	vector<string> state = get_system_state();
	vector<vector<vector<int>>> cars;
	string remainingCars;
	string newCar;

	//Parse state into vector of car data
	for (unsigned int i = 0; i < state.size(); i++){
		vector<vector<int>> carRow;
		remainingCars = state[i];
		remainingCars.push_back(';');

		//Parse string of entire lane into individual car data
		while (remainingCars.size() > 1) {
			remainingCars = remainingCars.substr(1);
			size_t pos = remainingCars.find(";");
			newCar = remainingCars.substr(1,pos-2);

			carRow.push_back(parse_car_data(newCar));

			if(pos!=string::npos){
				remainingCars = remainingCars.substr(pos);
			} else {
				remainingCars = "";
			}
		}
		cars.push_back(carRow);
	}
	return cars;
}

//Parse string in form (id,lane,pos,turn) into vector of ints
vector<int> TrafficModel::parse_car_data (string& car){
	vector<int> carData;
	string delimiter = ",";
	size_t last = 0;
	size_t next = 0;
	int index = 0;

	while ((next = car.find(delimiter, last)) != string::npos) {
		carData.push_back(stoi(car.substr(last, next-last)));
		last = next + 1;
		index++;
	}
	carData.push_back(stoi(car.substr(last)));
	return carData;
}

#include "Platoon.h"
#include <iostream>

Platoon::Platoon(string init)
{
    // the string 'init' looks like:
    // a,b ; c,d ; ... where, a and c are the vehicle id, b and d are positions.
    stringstream ss(init);
	string segment;
	while(getline(ss, segment, ';'))
	{
		size_t found = segment.find(",");
		if (found!=std::string::npos){
			string id = segment.substr(0, found);
			string pos = segment.substr(found+1, segment.size()-1);

			// conversion to integer
			stringstream s1(id);
			int id_value;
			s1 >> id_value;
			stringstream s2(pos);
			int pos_value;
			s2 >> pos_value;
			Car* car = new Car(id_value, pos_value);
      insert(car);
		}
	}
}

Car* Platoon::get_tail()
{
	return tail;
}

Car* Platoon::get_head()
{
	return head;
}

//Returns the number of cars in the linked list
int Platoon::get_size(){
  Car* currentCar = head;
  int size = 0;

  //Iterates through the list until there are no more cars
  while(currentCar!= NULL){
    size++;
    currentCar = currentCar->get_next();
  }
  return size;
}
/* This function was purely for testing purposes so that I could see the order of the cars within a platoon. It iterates through the list of cars, starting with the head node and moves backwards in terms of positions*/
void Platoon::printAll(){
  Car* currentCar = head;
  cout<<"Starting printall"<<endl;
  while(currentCar != NULL){
    cout << "Current cars positions: " << currentCar->get_position()<<endl; 
    currentCar = currentCar->get_next();
  }

}

void Platoon::remove(Car* c){
  //Must check for the edge case that the size is 1
  if(get_size() > 1){
    //Also check for the edge cases that occur when the car is the head or the tail
    if(c == head){
      c->get_next()->set_prev(NULL);
      head = c->get_next();
    }
    else if(c == tail)
    {
      c->get_prev()->set_next(NULL);
      tail = c->get_prev();  
    }
    else{
      //If the car is removed between 2 other cars, the cars are now put next to each other in queue
      c->get_prev()->set_next(c->get_next()); 
      c->get_next()->set_prev(c->get_prev());
    }
  }
  else{
    //If the size was 1 and we remove it, the head and tail are now null
    head = NULL;
    tail = NULL;
  }
  //In all cases, we will want to prevent the removed car from still pointing to the cars that used to be ahead/ behind it
  c->set_next(NULL);
  c->set_prev(NULL);
}

void Platoon::insert(Car* c){

  Car* currentCar = head;
  //Edge case for when inserting into an empty linked list
  if(get_size() == 0){
    tail = c;
    head = c;
  }
  else{
  //Iterate through the list until we find a car with a position smaller than the car to be inserted. Then insert in front of this car
    while(currentCar->get_position() > c->get_position() && currentCar != tail){
      currentCar = currentCar->get_next();
    }
  //If it reached the end of the list, it must determine if it places it in front of or behind the tail
  if(currentCar == tail && currentCar ->get_position() > c->get_position()){
    c->set_prev(tail);
    c->set_next(NULL);
    tail->set_next(c);
    tail = c;
    }
  else if(currentCar == NULL){
    c->set_prev(tail);
    c->set_next(NULL);
    tail->set_next(tail);
    tail = c;
    }
  else if(currentCar == head){
    //Case for when the car should be inserted at the front of the list
    head->set_prev(c);
    c->set_prev(NULL);
    c->set_next(head);
    head = c;
    }
  else{
    //Inserting between two cars
    c->set_prev(currentCar->get_prev());
    c->set_next(currentCar);
    currentCar->get_prev()->set_next(c);
    currentCar->set_prev(c);
    }
  }
}

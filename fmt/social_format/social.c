#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int state=1; // to start get the name

#define FIELDSIZE 0x100
typedef struct{
  char* name;
  char* description;
  size_t age;
} Person;

Person* create_person(void){
  Person* new_person=malloc(sizeof(Person));
  memset(new_person, 0, sizeof(Person));
  new_person->name=malloc(FIELDSIZE);
  memset(new_person->name,0,FIELDSIZE);
  new_person->description=malloc(FIELDSIZE);
  return new_person;
}

void delete_person(Person* p){
  free(p->name);
  free(p->description);
  free(p);
  return;
}
  
void get_name(Person* p){
  fprintf(stdout, "Name: ");
  fflush(NULL);
  fgets(p->name, FIELDSIZE, stdin);
  fflush(NULL);
  return;
}

void get_desc(Person* p){
  fprintf(stdout, "Description: ");
  fflush(NULL); 
  fgets(p->description, FIELDSIZE, stdin);
  fflush(NULL);
  fprintf(stdout, "Age: ");
  fflush(NULL); 
  char age[0x21];
  fgets(age, 0x20, stdin);
  fflush(NULL);
  p->age=atoi(age);
  return;
}

void print_details(Person* p,size_t age){
  fprintf(stdout, "Name: ");
  fprintf(stdout, p->name);
  puts("");
  fprintf(stdout, "Age: %d\n", age);
  fprintf(stdout, "Description: ");
  fprintf(stdout, p->description);
  puts("");
  fflush(NULL);
  return;
}


void display_menu(void){
  fprintf(stdout, "1.) Change your name\n"
	 "2.) Describe yourself\n"
	 "3.) Display all your information\n"
	 "4.) Exit the system\n"
	 );
  fflush(NULL);
  return;
}

void get_choice(void){
  char choice[21];
  fgets(choice,sizeof(choice)-1, stdin);
  puts("got your choice");
  fflush(NULL);
  int c=atoi(choice);
  switch(c){
  case 1://change name
    state=1;
    break;
  case 2://change desc
    state=2;
    break;
  case 3://display infos
    state=3;
    break;
  case 4://exit
    state=4;
    break;
  default:
    //big problem
    puts("You goofed!");
    fflush(NULL);
    state=4;
  }
  return;
}
void main_loop(Person* player){
  char key_buf[58];
  FILE* f_key=fopen("key","r");

  while(true){

    switch(state){
    case 0:
      state=4;
      fread(key_buf,56,1,f_key);
      key_buf[57] = 0;
      fprintf(stdout,"%s",key_buf);
      fflush(NULL);
      break;

    case 1://getname
      state=5;
      get_name(player);
      break;

    case 2:
      state=5;
      get_desc(player);
      break;

    case 3:
      state=5;
      print_details(player,player->age);
      break;

    case 4:
      puts("bye bye!");
      fflush(NULL);
      exit(1);
      break;

    case 5:
      state=6;
      display_menu();
      break;

    case 6:
      get_choice();//will set state
      break;
    default:
      state=4;
      fprintf(stdout, "state %d\n", state);
      puts("no no no no");
      fflush(NULL);
      break;
    }
    //printf("state %d\n",state);
  }
  return;
}

int main(int argc,char** argv){
  Person* player=create_person();
  puts("Welcome to mybookspacepage v00.01 Beta!");
  
  main_loop(player);
  
  delete_person(player);
  return 0; 
}

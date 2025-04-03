#include   <iostream>
#include   <fstream>
#include   <vector>
#include   <stack>
#include   <unordered_map>
#include   <algorithm>
using namespace  std;
class Parser{private:string code; 	int pointer	= 0;		bool	parse =
true;  string inputBuffer;		vector<int>	stack;	 unordered_map<int, int> heap;	
unordered_map<string, int>  labels;		bool done	=	false;	 static	bool
notspace(char c){return  !isspace(c);}	 int	read(){return code[pointer++];}	 int	readNum(){int sign
= read() == ' '	? 1:-1;		int	num =  0;
 while (true){num *=	2;  switch	(read()){case
 '\t':num++;  break;	 case	'\n':return	sign *
 num / 2;}}}		string	readLabel(){string label 	= ""; 
while (true){char c =	read();  if (c == '\n') return	label;
 label += c;}}	 int	inputChar(){if	(inputBuffer.length()	== 0) getline(cin,
inputBuffer);  char c	= inputBuffer[0];  inputBuffer.erase(inputBuffer.begin());	 return	c;}
 int  inputInt(){cout	<< "input:";	 if	(inputBuffer.length() == 0) getline(cin,
inputBuffer);  size_t n	 = inputBuffer.find_first_not_of("0123456789");	
n = n ==	-1 ?	inputBuffer.length():n; 	int	oup 
= 0;  for	(int	i =	0; i	<	n;
++i){oup = oup *	10	+	inputChar()	-	'0';}		return	oup;}
 int pop(){int val	=	stack[0];  stack.erase(stack.begin());	
return val;}  void	push(int	val){stack.insert(stack.begin(), val);}  void insert(int	i,
int val){stack.insert(stack.begin() + i,	val);}		void tlss(){if	(parse)	return;	
cout  << (char)	pop();} 	void	tlst(){if
(parse) return;  cout	<< pop();} 	void tlts(){if	(parse)
return;  int i	=	pop();  insert(i, inputChar());}  void tltt(){if
(parse) return;  int	i	= pop();	 insert(i,	inputInt());}		void
ss(){push(readNum());}  void sls(){push(stack[0]);}		void		sts(){int	n =	readNum(); 
push(stack[n]);}  void slt(){int	 temp =	stack[0];	 stack[0] =
stack[1];  stack[1] =	temp;}	 void		sll(){pop();}  void	stl(){/*TODO*/}
 void tts(){int 	value	= pop();	
int address = pop();
	heap[address]	=  value;}  void	ttt(){int	key =

pop();  push(heap[key]);} 
void  tsss(){if (parse)	return;
	int a =	pop(); 
int b = pop(); 
push(b	+
a);}		void	tsst(){if	(parse) return; 
int a
	= pop();	
int
b =
pop(); 
push(b
- a);} 	void
tssl(){if (parse)
return;

int a  = pop();
 int b =	pop();	 push(b	*
a);}		void	tsts(){if (parse) return; 	int	a 
=	pop(); 	int	b	=	pop();		push(b / a);}	 void tstt(){if (parse)	return;	 int	a
=	pop();		int  b =	pop();	 push(b	%
a);}	 void 
lss(){string	label = readLabel();	 labels[label] = pointer;}	
void		lst(){/*TODO*/}		void lsl(){string label  = readLabel(); 	if  (parse)  return;	 pointer	= labels[label];} 
void	 lts(){string label = readLabel();  if	(parse) return;  if (pop() == 0) pointer =
labels[label];}	 void	ltt(){string	label	=
readLabel();  if (parse) return; 	if	(pop() <	0)
pointer = labels[label];} 	void	ltl(){/*TODO*/} 	void
lll(){if	(parse)	return;	 done = true;}	
void	run(){string instruction = "";		while  (pointer
< code.length()
&&	!done){instruction += read();	
bool
success =
true;  if
(instruction
== "  ") ss(); 	else
if
(instruction
==
" \n ") sls(); 	else	if	(instruction	==	" \t ")	sts();  else
if (instruction	==	" \n\t")
slt();	else if	(instruction
==
" \n\n")	sll();		else if	(instruction == " \t\n") stl(); 	else
if
(instruction	==	"\t   ")	tsss(); 	else	if	(instruction == "\t  \t") tsst(); 	else	if	(instruction == "\t  \n") tssl();	 else if (instruction	==	"\t \t ")	tsts();  else
if	(instruction	== "\t \t\t") tstt(); 	else if	(instruction	=="\t\t ") tts(); else	if (instruction
==	"\t\t\t") ttt();  else if	(instruction	==	"\n  ")	lss();		else if	(instruction ==	"\n \t")	lst();	else	if	(instruction	==	"\n \n") lsl();	 else if (instruction	== "\n\t ") lts(); 	else	if	(instruction == "\n\t\t")	ltt();		else	if	(instruction	== "\n\t\n") ltl();  else if	(instruction ==
"\n\n\n") lll();		else if (instruction == "\t\n  ") tlss();		else	if (instruction ==	"\t\n \t")	tlst();
 else if (instruction	==	"\t\n\t ")	tlts();	
else	if	(instruction == "\t\n\t\t")	tltt();	else	success	=	false;  if (success){instruction	= "";}}} public:Parser(string	file){ifstream	t(file);	 string str((istreambuf_iterator<char>(t)),	istreambuf_iterator<char>());
 str.erase(remove_if(str.begin(), str.end(), notspace), str.end()); 
code	= str;  run();	 parse
= false;	
stack.clear();	 heap.clear(); 	pointer	=	0;		run();}}; int
main(){Parser	parser("Hello World.txt");		return 0;}
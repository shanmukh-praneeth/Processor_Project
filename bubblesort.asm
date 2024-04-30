#run in linux terminal by java -jar Mars4_5.jar nc filename.asm(take inputs from console)

#system calls by MARS simulator:
#http://courses.missouristate.edu/kenvollmar/mars/help/syscallhelp.html
.data
	next_line: .asciiz "\n"
	inp_statement: .asciiz "Enter No. of integers to be taken as input: "
	inp_int_statement: .asciiz "Enter starting address of inputs(in decimal format): "
	out_int_statement: .asciiz "Enter starting address of outputs (in decimal format): "
	enter_int: .asciiz "Enter the integer: "	
.text
#input: N= how many numbers to sort should be entered from terminal. 
#It is stored in $t1
jal print_inp_statement	
jal input_int 
move $t1,$t4			

#input: X=The Starting address of input numbers (each 32bits) should be entered from
# terminal in decimal format. It is stored in $t2
jal print_inp_int_statement
jal input_int
move $t2,$t4

#input:Y= The Starting address of output numbers(each 32bits) should be entered
# from terminal in decimal. It is stored in $t3
jal print_out_int_statement
jal input_int
move $t3,$t4 

#input: The numbers to be sorted are now entered from terminal.
# They are stored in memory array whose starting address is given by $t2
move $t8,$t3
move $s7,$zero	#i = 0
loop1:  beq $s7,$t1,loop1end
	jal print_enter_int
	jal input_int
	sw $t4,0($t2)
	sw $t4,0($t3)
	addi $t2,$t2,4
	addi $t3,$t3,4
      	addi $s7,$s7,1
        j loop1      
loop1end: move $t3,$t8       
#############################################################
#Do not change any code above this line
#Occupied registers $t1,$t2,$t3. Don't use them in your sort function.
#############################################################
#function: should be written by students(sorting function)
#The below function adds 10 to the numbers. You have to replace this with
#your code
addi $t5,$t3,0  #Address of input array is moved to register $t5

addi $t6,$zero,0
addi $s0,$t1,0  #Stores length of the array 
Sort_OuterLoop: 
	beq $s0,$t6,exit
	addi $t6,$t6,1
  addi $t7,$zero,0
	sub $s1,$s0,$t6
	addi $t9,$t5,0
	Sort_InnerLoop:	
		beq $t7,$s1,exitInner
		addi $t7,$t7,1
		lw $s4,0($t5)
		lw $s5,4($t5)
		ble $s4,$s5,nextElement
		addi $t8,$s4,0
		sw $s5,0($t5)
		sw $t8,4($t5)
		nextElement:
			addi $t5,$t5,4
			j Sort_InnerLoop 
	exitInner:
		addi $t5,$t9,0
		j Sort_OuterLoop
exit:	
	addi $t2,$t3,0
	
#endfunction
#############################################################
#You need not change any code below this line

#print sorted numbers
move $s7,$zero	#i = 0
loop: beq $s7,$t1,end
      lw $t4,0($t3)
      jal print_int
      jal print_line
      addi $t3,$t3,4
      addi $s7,$s7,1
      j loop 
#end
end:  li $v0,10
      syscall
#input from command line(takes input and stores it in $t6)
input_int: li $v0,5
	   syscall
	   move $t4,$v0
	   jr $ra
#print integer(prints the value of $t6 )
print_int: li $v0,1	
	   move $a0,$t4
	   syscall
	   jr $ra
#print nextline
print_line:li $v0,4
	   la $a0,next_line
	   syscall
	   jr $ra

#print number of inputs statement
print_inp_statement: li $v0,4
		la $a0,inp_statement
		syscall 
		jr $ra
#print input address statement
print_inp_int_statement: li $v0,4
		la $a0,inp_int_statement
		syscall 
		jr $ra
#print output address statement
print_out_int_statement: li $v0,4
		la $a0,out_int_statement
		syscall 
		jr $ra
#print enter integer statement
print_enter_int: li $v0,4
		la $a0,enter_int
		syscall 
		jr $ra
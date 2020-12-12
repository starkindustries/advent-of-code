DEBUG = True

def solvePart1(program):
    programCounter = 0
    accumulator = 0
    visited = set()
    while True:
        # Check for infinite loop
        if programCounter in visited:
            if DEBUG:
                print(f"About to execute instruction at {programCounter} a second time.")
                print(f"Current accumulator value: {accumulator}")
            return False
        else:
            visited.add(programCounter)

        # Process Instruction
        instruction = program[programCounter]
        op, arg = instruction.split(" ")
        arg = int(arg)                        
        if op == "nop":
            programCounter += 1
        elif op == "acc":
            accumulator += arg
            programCounter += 1
        elif op == "jmp":
            programCounter += arg        
        else:
            print(f"ERROR: unknown instruction: {instruction}")
            exit()
        
        # Check if end of program reached
        # From the challenge:
        # ********************************************************
        # "The program is supposed to terminate by attempting to 
        #  execute an instruction immediately after the last 
        #  instruction in the file"
        # ********************************************************
        if programCounter == len(program):
            print(f"Program exiting successfully. Counter at: {programCounter}.")
            print(f"Current accumulator value: {accumulator}")
            return True
        if programCounter > len(program):
            return False

program = []
with open("input.txt", "r") as handle:    
    for line in handle:
        line = line.strip()        
        program.append(line)

# Part 1
# print(program)
solvePart1(program)

# Part 2
print("==================================")
DEBUG = False
for i in range(len(program)):
    # Swap instructions
    if "nop" in program[i]:
        a, b = "nop", "jmp"        
    elif "jmp" in program[i]:
        a, b = "jmp", "nop"        
    else: # if no "nop" or "jmp" continue to next instruction
        continue

    program[i] = program[i].replace(a, b)
    
    # Test if contains infinite loop
    if solvePart1(program):
        print(f"Program fixed!")
        break
    else:
        # Test failed. Put program back to how it was.
        program[i] = program[i].replace(b, a)

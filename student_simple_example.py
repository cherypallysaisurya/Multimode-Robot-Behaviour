

from unified_robot import create_robot_program, run_with_visualization


def student_moves():


    program = create_robot_program(grid_width=6, grid_height=6, start_x=0, start_y=0, mode="simulator")
    

    program.add_wall(3, 3)
    program.add_wall(4, 3)
    program.add_wall(2, 4)
    
    def moves():
        program.robot.move("up")  
        program.robot.move("up") 
        program.robot.move("right")
        program.robot.move("right")     
        program.robot.move("down") 
        program.robot.move("down") 
        program.robot.move("left")
        program.robot.move("left")   
    # Run the moves
    run_with_visualization(program, moves)


if __name__ == "__main__":
   
    
    student_moves()

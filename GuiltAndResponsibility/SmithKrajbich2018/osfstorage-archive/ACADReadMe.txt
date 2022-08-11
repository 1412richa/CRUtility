Read me:

ACADchoiceandeyedata.RData

This contains data from each of the four choice tasks. The choice data is contained in the data frames with choicedata at the end of the names (e.g. twofoodchoicedata), and the eye tracking data in contained in the data frames with eyedata at the end of the names (e.g. foodriskeyedata). 

Variables:
SubjectNumber: subject numbers are consistent across tasks
Trial: the order in which subjects saw the choices
LeftRight: subject response (1 = left, 2 = right)
RT: response time in seconds
FoodLeft: index of food item presented on left side (in two-food task)
FoodRight: index of food item presented on right side (in two-food task)
FoodUpperLeft: index of food item presented in upper left corner (in food-risk task)
FoodUpperRight: index of food item presented in upper right corner (in food-risk task)
FoodLowerLeft: index of food item presented in lower left corner (in food-risk task)
FoodLowerRight: index of food item presented in lower right corner (in food-risk task)
ValueLeft: value of left option (in two-food task)
ValueRight: value of right option (in two-food task)
ValueUpperLeft: value of upper left food item/amount
ValueUpperRight: value of upper right food item/amount
ValueLowerLeft: value of lower left food item/amount
ValueLowerRight: value of lower right food item/amount
TopRowPayoffs: in social task, whose payoffs are in the top row (Me for self payoffs, You for other payoffs)
ROI: food/box on the screen that is the object of the current dwell (1 for upper left, 2 for upper right, 3 for lower left, 4 for lower right)
DwellLength: duration of dwell in seconds

ACADratingdata.RData

This contains the data from the food ratings task in a data frame called ratingdata.

Variables:
SubjectNumber: consistent from the other tasks
Food: index of food item currently being rated
Rating: subjective rating of food item
RT: response time in seconds

ACADvisualdata.RData

This contains the data from the psychophysical task in a data frame called visualdata.

Variables:
SubjectNumber: consistent from the other tasks
Response: subject response about direction of target stimulus (1 = up, 0 = down)
CorrectDirection: correct direction of target stimulus (1 = up, 0 = down)
RT: response time in seconds
Distance: distance from horizontal median (1 = near, 2 = middle, 3 = far)
Quadrant: quadrant of screen where target appeared (1 = upper left, 2 = upper right, 3 = lower left, 4 = lower right)
ISI: interstimulus interval between cue and stimulus presentation
Aborted: whether or not the trial was aborted due to the subject moving their eyes away from the central fixation point (1 = yes, 0 = no)






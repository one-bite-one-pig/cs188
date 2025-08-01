# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsulePos=successorGameState.getCapsules()

        "*** YOUR CODE HERE ***"

        x,y=newPos
        total=0
        newGhostPos=successorGameState.getGhostPositions()
        foodList=newFood.asList()

             
        for i in range(len(newGhostPos)):
            if newGhostPos[i]==newPos:
                if newScaredTimes[i]>0:
                    total+=5
                else:
                    return -float('inf')
            else:
                if newScaredTimes[i]==0:
                    gx,gy=newGhostPos[i]
                    d=abs(gx-x)+abs(gy-y)
                    if(d<=2):
                        total-=100/d
        
        for food in foodList:
            fx,fy=food
            d=abs(fx-x)+abs(fy-y)
            if d==0:
                total+=10
            else:
                total+=1/d
            
        total+= successorGameState.getScore()
        
        return total
        

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
 
        NumAgents=gameState.getNumAgents()
        
        def min_max(gamestate,index,depth):
            if gamestate.isWin() or gamestate.isLose() or depth==self.depth:
                return self.evaluationFunction(gamestate),None
            
            nextindex=(index+1)%NumAgents
            legalactions=gamestate.getLegalActions(index)
            
            nextdepth=depth
            if nextindex==0:
                nextdepth=depth+1
            
            if index==0:
                v=-float('inf')
                bestaction=legalactions[0]
                for action in legalactions:
                    next=gamestate.generateSuccessor(0,action)
                    nextvalue,_=min_max(next,nextindex,nextdepth)
                    if nextvalue>v:
                        v=nextvalue
                        bestaction=action
                return v, bestaction
            else:
                v=float('inf')
                bestaction=legalactions[0]
                for action in legalactions:
                    next=gamestate.generateSuccessor(index,action)
                    nextvalue,_=min_max(next,nextindex,nextdepth)
                    if nextvalue<v:
                        v=nextvalue
                        bestaction=action
                return v, bestaction
        _,action=min_max(gameState,0,0)
        return action
                
            
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        
        
        
        
        def a_b(gamestate,index,depth,a,b):
            if gamestate.isWin() or gamestate.isLose() or depth==self.depth:
                return self.evaluationFunction(gamestate),None
            
            
            NumAgents=gameState.getNumAgents()
            nextindex=(index+1)%NumAgents
            legalactions=gamestate.getLegalActions(index)
            
            nextdepth=depth
            if nextindex==0:
                nextdepth=depth+1
            
            if index==0:
                v=-float('inf')
                bestaction=None
                for action in legalactions:
                    next=gamestate.generateSuccessor(index,action)
                    nextvalue,_=a_b(next,nextindex,nextdepth,a,b)
                    if nextvalue>v:
                        v=nextvalue
                        bestaction=action
                    if v>b:
                        return v,bestaction
                    a=max(a,v)
                return v, bestaction
            else:
                v=float('inf')
                bestaction=None
                for action in legalactions:
                    next=gamestate.generateSuccessor(index,action)
                    nextvalue,_=a_b(next,nextindex,nextdepth,a,b)
                    if nextvalue<v:
                        v=nextvalue
                        bestaction=action
                    if a>v:
                        return v, bestaction
                    b=min(v,b)
                return v, bestaction
        _,action=a_b(gameState,0,0,-float('inf'),float('inf'))
        return action
                
        
        
        
        
        
        
        
        
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        NumAgents=gameState.getNumAgents()
        
        def max_exp(gamestate,index,depth):
            if gamestate.isWin() or gamestate.isLose() or depth==self.depth:
                return self.evaluationFunction(gamestate),None
            
            nextindex=(index+1)%NumAgents
            legalactions=gamestate.getLegalActions(index)
            
            nextdepth=depth
            if nextindex==0:
                nextdepth=depth+1
            
            if index==0:
                v=-float('inf')
                bestaction=legalactions[0]
                for action in legalactions:
                    next=gamestate.generateSuccessor(0,action)
                    nextvalue,_=max_exp(next,nextindex,nextdepth)
                    if nextvalue>v:
                        v=nextvalue
                        bestaction=action
                return v, bestaction
            else:
                total=0
                for action in legalactions:
                    next=gamestate.generateSuccessor(index,action)
                    nextvalue,_=max_exp(next,nextindex,nextdepth)
                    total+=nextvalue
                exp=total/len(legalactions)
                return exp, action[0]
        _,action=max_exp(gameState,0,0)
        return action
        
        
        util.raiseNotDefined()









def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score=currentGameState.getScore()
    Pos=currentGameState.getPacmanPosition()
    GPoss=currentGameState.getGhostPositions()
    foods=currentGameState.getFood()
    foodlist=foods.asList()
    capsules=currentGameState.getCapsules()
    ghosts = currentGameState.getGhostStates()
    
    x,y=Pos
    for ghost in ghosts:
        gpos = ghost.getPosition()
        distance = manhattanDistance(Pos, gpos)
        if ghost.scaredTimer == 0:
            if distance == 0:
                return -float('inf')  # eaten by ghost
            elif distance <= 2:
                score -= 8/ distance
            
            

            
    for food in foodlist:
            d=manhattanDistance(Pos,food)
            score+=3/d
    

    
    if capsules:
        min_capsule_distance = min(manhattanDistance(Pos, cap) for cap in capsules)
        score += 15 / min_capsule_distance
            
    
    return score
    
    
    
    
    
    
    
    
    
    
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

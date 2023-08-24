# wordle
wordle game, based on python Tkinter, including decision tree. 

File usage:

	main.py: 
		Main game code, to start game.

	InitialWordsAndDecisionTree.py: 
		To initial words and decision tree. Every time you change words_alpha.txt, you should run this file. 
		However, it will take a long time, maybe several hours, depends on your computer.

	GmeLogic.py: 
		Basic game logic, such as the judgement for the words and a filter for words.

	GenerateWidget.py: 
		To generate TKinter Widgets.
  
    words_alpha.txt: 
		To storage words.

Document usage: 
	
    WordsClassifiedByLength:
		Storage different length of words, generate by InitialWordsAndDecisionTree.py.
		This will update when you run InitialWordsAndDecisionTree.py.
		If you want to change the words, just alter words_alpha.txt, dont change this document.

	Trees: 
		Storage decision trees. Gv files are the description of the trees using graphviz. 
		PDF files are the visualization of the trees. It may take some minutes to open a PDF for the first time.

Versions: 
	
    graphviz==windows_10_msbuild_Release_graphviz-8.1.0-win32
	
    python==3.7.0
	
    pip==10.0.1
	    
       Tkinter==0.1.0
	    
       numpy==1.20.3
	    
       graphviz==0.20.1

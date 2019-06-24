##########
User Guide
##########

Basic Usage
-----------

This example uses the old API:

.. code-block:: python

   from boostsrl import boostsrl

   bk = boostsrl.example_data("background")
   background = boostsrl.modes(
	bk,
	["cancer"],
	useStdLogicVariables=True,
	treeDepth=4,
	nodeSize=2,
	numOfClauses=8
   )

   # Example Training Data
   train_pos = boostsrl.example_data("train_pos")
   train_neg = boostsrl.example_data("train_neg")
   train_facts = boostsrl.example_data("train_facts")

   model = boostsrl.train(background, train_pos, train_neg, train_facts)

   # Example Test Data
   test_pos = boostsrl.example_data("test_pos")
   test_neg = boostsrl.example_data("test_neg")
   test_facts = boostsrl.example_data("test_facts")

   test = boostsrl.test(model, test_pos, test_neg, test_facts)

   print("Training Time (s)", model.traintime())
   print("Results Summary  ", test.summarize_results())
   print("Inference Results", test.inference_results("cancer"))

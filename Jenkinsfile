pipeline
{
	
	agent any

	triggers
	{
		pollSCM("H/5 * * * *")
	}

	stages
	{
		stage("BUILD")
		{
			steps
			{
				echo "BUILD STARTED"				
				echo "BUILD COMPLETED"
			}
		}
		stage("TEST")
		{
			steps
			{
				echo "TEST STARTED"
				echo "TEST COMPLETED"
			}
		}
		stage("DEPLOY")
		{
			steps
			{
				echo "DEPLOYMENT STARTED"			
				echo "DEPLOYMENT COMPLETED"
			}
		}
	}
}

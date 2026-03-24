
import azure.functions as func
import azure.durable_functions as df

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# 1. CLIENT: Starts the orchestration
@myApp.route(route="start_orchestrator")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client: df.DurableOrchestrationClient):
    instance_id = await client.start_new("my_orchestrator")
    return client.create_check_status_response(req, instance_id)

# 2. ORCHESTRATOR: Coordinates the work
@myApp.orchestration_trigger(context_name="context")
def my_orchestrator(context: df.DurableOrchestrationContext):
    # Chain multiple activities
    result1 = yield context.call_activity("hello_activity", "Tokyo")
    result2 = yield context.call_activity("hello_activity", "Seattle")
    return [result1, result2]

# 3. ACTIVITY: Performs a single task
@myApp.activity_trigger(input_name="city")
def hello_activity(city: str):
    return f"Hello {city}!"

@myApp.orchestration_trigger(context_name="context")
def my_orchestrator(context: df.DurableOrchestrationContext):
    # Create a single object (dictionary) containing all variables
    input_data = {
        "city": "Seattle",
        "temperature": 25,
        "is_sunny": True
    }
    
    result = yield context.call_activity("multi_input_activity", input_data)
    return result
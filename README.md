# Retail-Queue-Management

Queue Management in Retail using Meraki MV Cameras

Customer satisfaction is a key care about for all retailers. According to research by uk.fashionnetwork.com long queues are among the chief contributors to lost store revenue, costing UK retailers up to £11.3 billion a year. In a blog post by qminder.com, on average 73% of shoppers would abandon their purchase if they had to queue for more than five minutes. 

Most, if not all major retailers, have physical security cameras monitoring many aspects of the store including checkout queues. However, most don’t have the inbuilt analytics to identify a person within the frame or within a specific zone of the frame.

The Cisco Meraki MV series of cameras have the ability to identify a person within a frame without breaching privacy as this does not use facial recognition technology but rather, people and object detection.

The information on objects within the video can be accessed using REST API calls without the need to stream any video footage or use CPU intensive image analysis engines.
The capability makes people counting and queue length identification an easy task.

We can see an example of a REST API call to an MV camera requesting Live Analytics of the image and any zones configured within the image.

This will return a JSON response detailing the objects detected

{
    "ts": "2020-03-25T17:12:46.611Z",
    "zones": {
        "701234567890123456": {
            "person": 0
        },
        "701234567890123457": {
            "person": 1
        },
        "701234567890123458": {
            "person": 0
        },



Using a simple python program, it is possible to identify when the number of customers queuing is over the desired amount. This program can then request the camera to take a Snapshot (image) via the REST API POST call

We now need to inform the retail store management and staff that there is a large queue that need to be attended to by either opening another checkout or attending to customers with mobile checkout terminal.



Cisco Webex teams is an idea application that can reside on a variety of operating systems including Windows, Apple iOS and Android to name a few.  Within Webex teams we can create a number of spaces and rooms that we can align to the different retailer store teams and also the types of queues in the store, such as self-checkout, one basket and standard checkouts.

The information about checkout queues can then be published to these rooms along with a picture (if appropriate) of the queue. The information is only published if there is a queue over a certain number of people or if a certain waiting time times is superseded. This means that the Webex Teams rooms are not constantly filling with checkout queue information, only when necessary. 
The store staff are also responding to these checkout queue alerts, by detailing what they have done to reduce the queues, thus giving a record of the queues and the actions taken.

We are able to use the comprehensive REST APIs that are available for Webex Teams to achieve this from the same Python code we are running to identify the queue.

The Python code creates a message with the details of the queue and includes the snapshot of the queue (if appropriate)

The following diagram give an overview of the REST API calls and the overall flow of the solution.

 

This is just one example in a retail setting of the power that the Meraki MV Camera analytics gives. There are many more use cases across many customers where we can apply the same principles to look at security, building occupancy, trespass and COVID-19 social distancing to name a few

To find out more about the Meraki MV Cameras go here https://meraki.cisco.com/products/security-cameras


To find out more about Meraki MV Object Detection go here
https://documentation.meraki.com/MV/Video_Analytics/MV_Object_Detection


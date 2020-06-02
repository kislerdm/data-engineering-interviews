# Message broker

<table>
   <tr>
      <td>⚠️</td>
      <td>
         The answers here are given by the community. Be careful and double check the answers before using them. <br>
         If you see an error, please create a PR with a fix.
      </td>
   </tr>
</table>

**Legend**: 👶 easy ‍⭐️ medium 🚀 expert

<!-- content -->

### What is Quality of Service? 👶

The Quality of Service (QoS) level is a sender-receiver agreement to define the guarantee of a message delivery.

The following *three level of QoS* are usually being defined:

- At most once, *QoS0*
- At least once, *QoS1*
- Exactly once, *QoS2*

#### QoS0

At most once, or 'fire and forget' level guarantees a best-effort delivery and provides the same level of guarantee as the underlying transmission protocol (e.g. TCP).
A client won't receive any confirmation from the broker upon receipt. Likewise a message delivered to a client from the broker is not required to be acknowledged. This is the fastest way to publish and receive messages, but also the one where message loss is most likely to happen.

##### When to use

- When the network connection between sender and receiver is stable

- Occasional loss of few messages is acceptable when the data is not important or when data is sent at short intervals

- No message queuing required

#### QoS1

A client will receive a confirmation message from the broker upon receipt. If the expected confirmation is not received within a certain time frame, the client has to retry the message. A message received by a client must be acknowledged on time as well, otherwise the broker will re-deliver the message.

##### When to use

- No message loss is acceptable and duplicates can be handled

- The overhead of *QoS2* is unbearable. *QoS1* delivers messages much faster than *QoS2*.

#### QoS2
This level guarantees that each message is received only once by the intended recipients. It is the safest and slowest quality of service level. The guarantee is provided by at least two request/response flows (a four-part handshake) between the sender and the receiver.

##### When to use

- It is critical to your application to receive all messages exactly once, e.g. when handling purchase transactions


***References***:

- https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/

- https://vernemq.com/intro/mqtt-primer/quality_of_service.html

### Explain how kafka works? ‍⭐

TBD

***References***:

- link1

- link2

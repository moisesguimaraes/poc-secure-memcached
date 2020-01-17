# Memcached hardening for python services and applications.

## The problem

Whenever deploying a service inside a network, basic security concerns come to mind:

* Is the network trusted? Can we send data in plaintext?
* Is the service available only to those intended to use it?
* Can the service itself or others have access to the data?

## Possible solutions

### Protecting data in transit using TLS

Since version 1.5.13, Memcached supports authentication and encryption via TLS. This feature requires:

* OpenSSL 1.1.0 or later;
* A Memcached client with TLS support;
* A Memcached server built using `./configure --enable-tls`.

Encrypting the trafic protects the data in transit from reading and tampering. The complexity impact is that each Memcached server will need a valid certificate. The performance impact is the TLS overhead itself.

Performing client authentication protects the server from unauthorized read and write operations. The complexity impact is that each Memcached client will need a valid certificate. The performance impact is bigger due to extra steps to authenticate both sides.

This approach doesn't protects the data held in memory by Memcached in any other way.

### Restricting access to Memcached using SASL

Since version 1.4.3, Memcached supports authentication via SASL. This feature requires:

* A Memcached client with SASL support;
* A Memcached server built using `./configure --enable-sasl`.

This approach protects the server from unauthorized read and write operations. The complexity and performance impact is according to the SASL usage.

This approach doesn't protects the data in transit or held in memory by Memcached in any other way.

### Encrypting data before storing it in Memcached

This approach consists of encrypting the data before sending it to Memcached. The complexity impact is dealing with key sharing for the encryption/decryption process. The performance impact depends on the algorithms used for encryption.

This approach protects the data both in transit and held in memory by Memcached, but the key sharing is more prone to setup errors than the TLS or the SASL approach.

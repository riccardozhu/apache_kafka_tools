# Distribuzione dell'infrastruttura Kafka su macchine

## 1. Cluster ZooKeeper (3 macchine)
- **Macchina ZK1:**
  - ZooKeeper Node 1
  - JMX Exporter per metriche

- **Macchina ZK2:**
  - ZooKeeper Node 2
  - JMX Exporter per metriche

- **Macchina ZK3:**
  - ZooKeeper Node 3
  - JMX Exporter per metriche

## 2. Cluster Kafka (3 macchine)
- **Macchina KB1:**
  - Kafka Broker 1
  - JMX Exporter per metriche

- **Macchina KB2:**
  - Kafka Broker 2
  - JMX Exporter per metriche

- **Macchina KB3:**
  - Kafka Broker 3
  - JMX Exporter per metriche

## 3. Monitoraggio e Gestione (2 macchine)
- **Macchina MON:**
  - Prometheus
  - Grafana

- **Macchina MGT:**
  - Kafka Manager o Confluent Control Center

## 4. Sicurezza e Servizi Ausiliari (1 macchina)
- **Macchina SEC:**
  - Servizio di gestione certificati
  - Firewall centrale (se applicabile)
  - Sistema di logging centralizzato

## 5. Backup e Disaster Recovery (1 macchina)
- **Macchina BDR:**
  - Sistema di backup
  - Componenti di disaster recovery

## Totale: 10 macchine

Note:
- Ogni macchina dovrebbe avere il proprio firewall locale configurato.
- La configurazione SASL_SSL e le ACL sono distribuite su tutti i nodi Kafka e ZooKeeper.
- I client Kafka (produttori/consumatori) non sono inclusi in questa distribuzione in quanto tipicamente risiedono su macchine separate o nelle applicazioni degli utenti.

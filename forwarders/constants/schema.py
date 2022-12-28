# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Forwarder schema constants to be used across the project."""

KEY_FORWARDERS = "forwarders"
KEY_NAME = "name"
KEY_COLLECTORS = "collectors"
KEY_DISPLAY_NAME = "displayName"
KEY_CONFIG = "config"
KEY_RESPONSE_CODE = "responseCode"
KEY_STATE = "state"
KEY_UPLOAD_COMPRESSION = "uploadCompression"
KEY_METADATA = "metadata"
KEY_ASSET_NAMESPACE = "assetNamespace"
KEY_REGEX_FILTER = "regexFilter"
KEY_DESCRIPTION = "description"
KEY_REGEXP = "regexp"
KEY_BEHAVIOR = "behavior"
KEY_SERVER_SETTINGS = "serverSettings"
KEY_GRACEFUL_TIMEOUT = "gracefulTimeout"
KEY_DRAIN_TIMEOUT = "drainTimeout"
KEY_HTTP_SETTINGS = "httpSettings"
KEY_PORT = "port"
KEY_HOST = "host"
KEY_READ_TIMEOUT = "readTimeout"
KEY_WRITE_TIMEOUT = "writeTimeout"
KEY_READ_HEADER_TIMEOUT = "readHeaderTimeout"
KEY_IDLE_TIMEOUT = "idleTimeout"
KEY_ROUTE_SETTINGS = "routeSettings"
KEY_AVAILABLE_STATUS_CODE = "availableStatusCode"
KEY_READY_STATUS_CODE = "readyStatusCode"
KEY_UNREADY_STATUS_CODE = "unreadyStatusCode"
KEY_LOG_TYPE = "logType"
KEY_DISK_BUFFER = "diskBuffer"
KEY_DIRECTORY_PATH = "directoryPath"
KEY_MAX_FILE_BUFFER_BYTES = "maxFileBufferBytes"
KEY_MAX_SECONDS_PER_BATCH = "maxSecondsPerBatch"
KEY_MAX_BYTES_PER_BATCH = "maxBytesPerBatch"
KEY_FILE_PATH = "filePath"
KEY_FILE_SETTINGS = "fileSettings"
KEY_KAFKA_SETTINGS = "kafkaSettings"
KEY_USERNAME = "username"
KEY_PASSWORD = "password"
KEY_TOPIC = "topic"
KEY_GROUP_ID = "groupId"
KEY_TIMEOUT = "timeout"
KEY_BROKERS = "brokers"
KEY_TLS_SETTINGS = "tlsSettings"
KEY_CERTIFICATE = "certificate"
KEY_CERTIFICATE_KEY = "certificateKey"
KEY_MINIMUM_TLS_VERSION = "minimumTlsVersion"
KEY_INSECURE_SKIP_VERIFY = "insecureSkipVerify"
KEY_AUTHENTICATION = "authentication"
KEY_PCAP_SETTINGS = "pcapSettings"
KEY_NETWORK_INTERFACE = "networkInterface"
KEY_BPF = "bpf"
KEY_SPLUNK_SETTINGS = "splunkSettings"
KEY_MINIMUM_WINDOW_SIZE = "minimumWindowSize"
KEY_MAXIMUM_WINDOW_SIZE = "maximumWindowSize"
KEY_QUERY_STRING = "queryString"
KEY_QUERY_MODE = "queryMode"
KEY_CERT_IGNORED = "certIgnored"
KEY_SYSLOG_SETTINGS = "syslogSettings"
KEY_PROTOCOL = "protocol"
KEY_ADDRESS = "address"
KEY_BUFFER_SIZE = "bufferSize"
KEY_CONNECTION_TIMEOUT = "connectionTimeout"
KEY_RESPONSE_CODE = "responseCode"
ROW_AVAILABLE_STATUS_CODE = (
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS][ROUTE_SETTINGS]"
    " Available status code")
FORWARDER_COLUMN_HEADER = [
    "ID", "Display name", "Forwarder state", "[CONFIG] Upload compression",
    "[CONFIG][METADATA] Asset namespace", "[CONFIG][METADATA] Labels",
    "[CONFIG] Regex filters", "[CONFIG][SERVER_SETTINGS] Server state",
    "[CONFIG][SERVER_SETTINGS] Graceful timeout",
    "[CONFIG][SERVER_SETTINGS] Drain timeout",
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS] Port",
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS] Host",
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS] Read timeout",
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS] Read header timeout",
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS] Write timeout",
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS] Idle timeout",
    ROW_AVAILABLE_STATUS_CODE,
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS][ROUTE_SETTINGS] Ready status code",
    "[CONFIG][SERVER_SETTINGS][HTTP_SETTINGS][ROUTE_SETTINGS] Unready status code"
]
COLLECTOR_COLUMN_HEADER = [
    "Forwarder ID", "Collector ID", "Display Name", "Collector state",
    "[CONFIG] Log type", "[CONFIG] Max seconds per batch",
    "[CONFIG] Max bytes per batch", "[CONFIG][METADATA] Asset namespace",
    "[CONFIG][METADATA] Labels", "[CONFIG] Regex filters",
    "[CONFIG][DISK_BUFFER] State", "[CONFIG][DISK_BUFFER] Directory path",
    "[CONFIG][DISK_BUFFER] Max file buffer bytes",
    "[CONFIG][FILE_SETTINGS] File path",
    "[CONFIG][KAFKA_SETTINGS][AUTHENTICATION] username",
    "[CONFIG][KAFKA_SETTINGS][AUTHENTICATION] password",
    "[CONFIG][KAFKA_SETTINGS] Topic", "[CONFIG][KAFKA_SETTINGS] Group id",
    "[CONFIG][KAFKA_SETTINGS] Timeout", "[CONFIG][KAFKA_SETTINGS] Brokers",
    "[CONFIG][KAFKA_SETTINGS][TLS_SETTINGS] Certificate",
    "[CONFIG][KAFKA_SETTINGS][TLS_SETTINGS] Certificate key",
    "[CONFIG][KAFKA_SETTINGS][TLS_SETTINGS] Minimum tls version",
    "[CONFIG][KAFKA_SETTINGS][TLS_SETTINGS] Insecure skip verify",
    "[CONFIG][PCAP_SETTINGS] Network interface", "[CONFIG][PCAP_SETTINGS] Bpf",
    "[CONFIG][SPLUNK_SETTINGS][AUTHENTICATION] username",
    "[CONFIG][SPLUNK_SETTINGS][AUTHENTICATION] Password",
    "[CONFIG][SPLUNK_SETTINGS] Host", "[CONFIG][SPLUNK_SETTINGS] Port",
    "[CONFIG][SPLUNK_SETTINGS] Minimum window size",
    "[CONFIG][SPLUNK_SETTINGS] Maximum windows size",
    "[CONFIG][SPLUNK_SETTINGS] Query string",
    "[CONFIG][SPLUNK_SETTINGS] Query mode",
    "[CONFIG][SPLUNK_SETTINGS] Cert ignored",
    "[CONFIG][SYSLOG_SETTINGS] Protocol", "[CONFIG][SYSLOG_SETTINGS] Address",
    "[CONFIG][SYSLOG_SETTINGS] Port", "[CONFIG][SYSLOG_SETTINGS] Buffer size",
    "[CONFIG][SYSLOG_SETTINGS] Connection timeout",
    "[CONFIG][SYSLOG_SETTINGS][TLS_SETTINGS] Certificate",
    "[CONFIG][SYSLOG_SETTINGS][TLS_SETTINGS] Certificate key",
    "[CONFIG][SYSLOG_SETTINGS][TLS_SETTINGS] Minimum tls version",
    "[CONFIG][SYSLOG_SETTINGS][TLS_SETTINGS] Insecure skip verify"
]
KEY_FORWARDER_SCHEMA = "forwarderSchema"
KEY_COLLECTOR_SCHEMA = "collectorSchema"
KEY_FIELD_TYPE = "type"
KEY_FIELD_PATH = "fieldPath"
ENUM_FIELD_TYPE = "ENUM"
INT_FIELD_TYPE = "INT"
STRING_FIELD_TYPE = "STRING"
LABEL_FIELD_TYPE = "LABEL"
ONEOF_FIELD_TYPE = "ONEOF"
KEY_ENUM_FIELD_SCHEMAS = "enumFieldSchemas"
KEY_ONEOF_FIELD_SCHEMAS = "oneOfFieldSchemas"
BOOL_FIELD_TYPE = "BOOL"
KEY_IS_REQUIRED = "isRequired"
KEY_VALUE = "value"
KEY_IS_REPEATED = "isRepeated"
KEY_DEFAULT_VALUE = "defaultValue"
STR_SECRET_FIELD_TYPE = "STRING_SECRET"
REPEATED_STRING_FIELD_TYPE = "REPEATED_STRING"
KEY_INGESTION_SETTINGS = "ingestion settings"
TLS_SETTINGS_FIELD_PATH = "tls_settings"
CONNECTION_TIMEOUT_FIELD_PATH = "connection_timeout"
PROTOCOL_FIELD_PATH = "protocol"
KEY_ID = "ID"
SENSITIVE_FIELDS = ["password"]
KEY_AUTH = "auth"

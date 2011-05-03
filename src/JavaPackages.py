java_packages = {
    # Names that are defined in standard java packages.
    # Used to determine the use of 'self.' prefix
    'java.io': [
        # Interfaces
        "DataInput",
        "DataOutput",
        "Externalizable",
        "FileFilter",
        "FilenameFilter",
        "ObjectInput",
        "ObjectInputValidation",
        "ObjectOutput",
        "ObjectStreamConstants",
        "Serializable",
        # Classes
        "BufferedInputStream",
        "BufferedOutputStream",
        "BufferedReader",
        "BufferedWriter",
        "ByteArrayInputStream",
        "ByteArrayOutputStream",
        "CharArrayReader",
        "CharArrayWriter",
        "DataInputStream",
        "DataOutputStream",
        "File",
        "FileDescriptor",
        "FileInputStream",
        "FileOutputStream",
        "FilePermission",
        "FileReader",
        "FileWriter",
        "FilterInputStream",
        "FilterOutputStream",
        "FilterReader",
        "FilterWriter",
        "InputStream",
        "InputStreamReader",
        "LineNumberInputStream",
        "LineNumberReader",
        "ObjectInputStream",
        "ObjectInputStream.GetField",
        "ObjectOutputStream",
        "ObjectOutputStream.PutField",
        "ObjectStreamClass",
        "ObjectStreamField",
        "OutputStream",
        "OutputStreamWriter",
        "PipedInputStream",
        "PipedOutputStream",
        "PipedReader",
        "PipedWriter",
        "PrintStream",
        "PrintWriter",
        "PushbackInputStream",
        "PushbackReader",
        "RandomAccessFile",
        "Reader",
        "SequenceInputStream",
        "SerializablePermission",
        "StreamTokenizer",
        "StringBufferInputStream",
        "StringReader",
        "StringWriter",
        "Writer",
        # Exceptions
        "CharConversionException",
        "EOFException",
        "FileNotFoundException",
        "InterruptedIOException",
        "InvalidClassException",
        "InvalidObjectException",
        "IOException",
        "NotActiveException",
        "NotSerializableException",
        "ObjectStreamException",
        "OptionalDataException",
        "StreamCorruptedException",
        "SyncFailedException",
        "UnsupportedEncodingException",
        "UTFDataFormatException",
        "WriteAbortedException",
    ],
    'java.lang': [
        # Interfaces
        "CharSequence",
        "Cloneable",
        "Comparable",
        "Runnable",
        # Classes
        "Boolean",
        "Byte",
        "Character",
        "Character.Subset",
        "Character.UnicodeBlock",
        "Class",
        "ClassLoader",
        "Compiler",
        "Double",
        "Float",
        "InheritableThreadLocal",
        "Integer",
        "Long",
        "Math",
        "Number",
        "Object",
        "Package",
        "Process",
        "Runtime",
        "RuntimePermission",
        "SecurityManager",
        "Short",
        "StackTraceElement",
        "StrictMath",
        "String",
        "StringBuffer",
        "System",
        "Thread",
        "ThreadGroup",
        "ThreadLocal",
        "Throwable",
        "Void",
        # Exceptions
        "ArithmeticException",
        "ArrayIndexOutOfBoundsException",
        "ArrayStoreException",
        "ClassCastException",
        "ClassNotFoundException",
        "CloneNotSupportedException",
        "Exception",
        "IllegalAccessException",
        "IllegalArgumentException",
        "IllegalMonitorStateException",
        "IllegalStateException",
        "IllegalThreadStateException",
        "IndexOutOfBoundsException",
        "InstantiationException",
        "InterruptedException",
        "NegativeArraySizeException",
        "NoSuchFieldException",
        "NoSuchMethodException",
        "NullPointerException",
        "NumberFormatException",
        "RuntimeException",
        "SecurityException",
        "StringIndexOutOfBoundsException",
        "UnsupportedOperationException",
        # Errors
        "AbstractMethodError",
        "AssertionError",
        "ClassCircularityError",
        "ClassFormatError",
        "Error",
        "ExceptionInInitializerError",
        "IllegalAccessError",
        "IncompatibleClassChangeError",
        "InstantiationError",
        "InternalError",
        "LinkageError",
        "NoClassDefFoundError",
        "NoSuchFieldError",
        "NoSuchMethodError",
        "OutOfMemoryError",
        "StackOverflowError",
        "ThreadDeath",
        "UnknownError",
        "UnsatisfiedLinkError",
        "UnsupportedClassVersionError",
        "VerifyError",
        "VirtualMachineError",
    ],
    'java.net': [
        # Interfaces
        "ContentHandlerFactory",
        "DatagramSocketImplFactory",
        "FileNameMap",
        "SocketImplFactory",
        "SocketOptions",
        "URLStreamHandlerFactory",
        # Classes
        "Authenticator",
        "ContentHandler",
        "DatagramPacket",
        "DatagramSocket",
        "DatagramSocketImpl",
        "HttpURLConnection",
        "Inet4Address",
        "Inet6Address",
        "InetAddress",
        "InetSocketAddress",
        "JarURLConnection",
        "MulticastSocket",
        "NetPermission",
        "NetworkInterface",
        "PasswordAuthentication",
        "ServerSocket",
        "Socket",
        "SocketAddress",
        "SocketImpl",
        "SocketPermission",
        "URI",
        "URL",
        "URLClassLoader",
        "URLConnection",
        "URLDecoder",
        "URLEncoder",
        "URLStreamHandler",
        # Exceptions
        "BindException",
        "ConnectException",
        "MalformedURLException",
        "NoRouteToHostException",
        "PortUnreachableException",
        "ProtocolException",
        "SocketException",
        "SocketTimeoutException",
        "UnknownHostException",
        "UnknownServiceException",
        "URISyntaxException",
    ],
    'java.text': [
        # Interfaces
        "AttributedCharacterIterator",
        "CharacterIterator",
        # Classes
        "Annotation",
        "AttributedCharacterIterator.Attribute",
        "AttributedString",
        "Bidi",
        "BreakIterator",
        "ChoiceFormat",
        "CollationElementIterator",
        "CollationKey",
        "Collator",
        "DateFormat",
        "DateFormat.Field",
        "DateFormatSymbols",
        "DecimalFormat",
        "DecimalFormatSymbols",
        "FieldPosition",
        "Format",
        "Format.Field",
        "MessageFormat",
        "MessageFormat.Field",
        "NumberFormat",
        "NumberFormat.Field",
        "ParsePosition",
        "RuleBasedCollator",
        "SimpleDateFormat",
        "StringCharacterIterator",
        # Exceptions
        "ParseException",
    ],
    'java.util': [
        # Interfaces
        'Collection',
        'Comparator',
        'Enumeration',
        'EventListener',
        'Iterator',
        'List',
        'ListIterator',
        'Map',
        'Map.Entry',
        'Observer',
        'RandomAccess',
        'Set',
        'SortedMap',
        'SortedSet',
        # Classes
        'AbstractCollection',
        'AbstractList',
        'AbstractMap',
        'AbstractSequentialList',
        'AbstractSet',
        'ArrayList',
        'Arrays',
        'BitSet',
        'Calendar',
        'Collections',
        'Currency',
        'Date',
        'Dictionary',
        'EventListenerProxy',
        'EventObject',
        'GregorianCalendar',
        'HashMap',
        'HashSet',
        'Hashtable',
        'IdentityHashMap',
        'LinkedHashMap',
        'LinkedHashSet',
        'LinkedList',
        'ListResourceBundle',
        'Locale',
        'Observable',
        'Properties',
        'PropertyPermission',
        'PropertyResourceBundle',
        'Random',
        'ResourceBundle',
        'SimpleTimeZone',
        'Stack',
        'StringTokenizer',
        'Timer',
        'TimerTask',
        'TimeZone',
        'TreeMap',
        'TreeSet',
        'Vector',
        'WeakHashMap',
        # Exceptions
        'ConcurrentModificationException',
        'EmptyStackException',
        'MissingResourceException',
        'NoSuchElementException',
        'TooManyListenersException',
    ],
}

flowchart TD
    A[Start: Terminal Idle] --> B{Motion Detected?}
    B -- No --> A
    B -- Yes --> C[Wake Screen: Show Welcome Screen]

    C --> D{Voice Prompt or Keyboard Press?}
    D -- None after Timeout --> A
    D -- Activated --> E[Prompt for Student Credentials]

    E --> F[Student Enters Credentials]
    F --> G[Authenticate and Access Student Info DB]

    G --> H{Authentication Success?}
    H -- No --> I[Show Error and Retry or Guest Access]
    H -- Yes --> J[Access Student Database and Load Student Profile & Main Menu]

    J --> K{Select a Service}
    K --> L[LLM Powered Advising Assistant Conversation Start]
    K --> M[Service B]
    K --> N[Service C]
    K --> O[Service D]
    K --> P[Service E]

    L --> LA[Perform Conversation and Display]
    LA --> L
    M --> MB[Perform Task and Display Results]
    N --> NC[Perform Task and Display Results]
    O --> OD[Perform Task and Display Results]
    P --> PE[Perform Task and Display Results]

    LA & MB & NC & OD & PE --> Q{User Done?}
    Q -- No --> J
    Q -- Yes --> R[Log Out Student Profile]

    R --> S{Motion Detected within Timeout?}
    S -- No --> T[Dim Screen and Return to Idle Loop]
    S -- Yes --> J

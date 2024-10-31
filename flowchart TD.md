```mermaid
flowchart TD
    subgraph Data Sources
        S1[Sensors] -->|Raw Data| C1
        S2[Computing Systems] -->|Logs| C1
        S3[Processed Data] -->|Analytics| C1
        V1[Video Cameras] -->|Raw Video| V2
    end

    subgraph Video Processing
        V2[Video Collector]
        V2 -->|Buffer| V3[Video Queue]
        V3 -->|Stream| V4[Video Processor]
        V4 -->|Clips| V5[Video Segmentation]
        V4 -->|Metadata| C1
        V5 -->|Store| D4[(Video Store)]
        V5 -->|Thumbnails| D2[(Object Storage)]
    end

    subgraph Data Collection
        C1[Data Collectors/Agents]
        C1 -->|Buffer| C2[Message Queue]
        C2 -->|Stream| P1
    end

    subgraph Processing Layer
        P1[Data Processor]
        P1 -->|Transform| P2[Data Validator]
        P2 -->|Clean| P3[Data Enricher]
    end

    subgraph Storage Layer
        P3 -->|Write| D1[(Time-series DB)]
        P3 -->|Archive| D2
        P3 -->|Index| D3[(Search Index)]
    end

    subgraph ML Pipeline
        M1[Feature Extraction] -->|Process| M2[Model Training]
        M2 -->|Deploy| M3[Inference Service]
        D4 -->|Feed| M1
        D1 -->|Feed| M1
        M3 -->|Results| P3
    end

    subgraph Analysis Layer
        D1 --> A1[Real-time Dashboard]
        D2 --> A2[Batch Analysis]
        D3 --> A3[Log Search]
        D4 --> A4[Video Analysis UI]
    end
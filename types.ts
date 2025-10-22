
export interface GleifLegalName {
  name: string;
  language: string;
}

export interface GleifEntity {
  legalName: GleifLegalName;
  legalAddress: {
    addressLines: string[];
    city: string;
    region: string;
    country: string;
    postalCode: string;
  };
}

export interface GleifRecordAttributes {
  lei: string;
  entity: GleifEntity;
}

export interface GleifRecord {
  id: string;
  type: string;
  attributes: GleifRecordAttributes;
}

export interface GleifApiResponse {
  data: GleifRecord[];
}

export interface GroundingChunkWeb {
    uri: string;
    title: string;
}

export interface GroundingChunk {
    web: GroundingChunkWeb;
}

export interface GeminiVerificationResult {
    legalName: string;
    sources: GroundingChunk[];
}

export interface LEIData {
  lei: string;
  legalName: string;
  address: string;
  sources: GroundingChunk[];
}

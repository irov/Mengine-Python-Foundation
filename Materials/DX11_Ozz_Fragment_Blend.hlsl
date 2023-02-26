sampler2D tex0;

struct v2p {
    float4 position  : POSITION;
    float4 color : COLOR0;
    float2 tex0 : TEXCOORD0;
};

struct p2f {
    float4 color : COLOR0;
};
  
void main(in v2p IN, out p2f OUT)
{
    float4 color = tex2D(tex0, IN.tex0);
    OUT.color = IN.color * color;
}

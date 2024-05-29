<%
    import datetime
    protover = config.rfnoc_version.split('.')
    protover_major = protover[0];
    protover_minor = protover[1];
%>//
// Copyright ${datetime.datetime.now().year} ${config.copyright}
//
// ${config.license}
//
// Header: rfnoc_image_core.vh (for ${config.device.type})
//
// Description:
//
//   This is the header file for the RFNoC Image Core.
//
//   This file was automatically generated by the RFNoC image builder tool.
//   Re-running that tool will overwrite this file!
//
// File generated on: ${datetime.datetime.now().isoformat()}
% if source:
// Source: ${source}
% endif
% if source_hash:
// Source SHA256: ${source_hash}
% endif
//

`define CHDR_WIDTH     ${config.chdr_width}
`define RFNOC_PROTOVER { 8'd${protover_major}, 8'd${protover_minor} }

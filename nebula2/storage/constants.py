#
# Autogenerated by Thrift
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#  @generated
#

from __future__ import absolute_import
import six
import sys
from nebula2.fbthrift.util.Recursive import fix_spec
from nebula2.fbthrift.Thrift import TType, TMessageType, TPriority, TRequestContext, TProcessorEventHandler, TServerInterface, TProcessor, TException, TApplicationException, UnimplementedTypedef
from nebula2.fbthrift.protocol.TProtocol import TProtocolException


import nebula2.common.ttypes
import nebula2.meta.ttypes


from .ttypes import UTF8STRINGS, StatType, OrderDirection, EdgeDirection, ScanType, EngineSignType, RequestCommon, PartitionResult, ResponseCommon, StatProp, Expr, EdgeProp, VertexProp, OrderBy, TraverseSpec, GetNeighborsRequest, GetNeighborsResponse, ExecResponse, GetPropRequest, GetPropResponse, NewTag, NewVertex, EdgeKey, NewEdge, AddVerticesRequest, AddEdgesRequest, DeleteVerticesRequest, DeleteEdgesRequest, DelTags, DeleteTagsRequest, UpdateResponse, UpdatedProp, UpdateVertexRequest, UpdateEdgeRequest, GetUUIDReq, GetUUIDResp, LookupIndexResp, IndexColumnHint, IndexQueryContext, IndexSpec, LookupIndexRequest, LookupAndTraverseRequest, ScanVertexRequest, ScanVertexResponse, ScanEdgeRequest, ScanEdgeResponse, TaskPara, AddAdminTaskRequest, StopAdminTaskRequest, AdminExecResp, TransLeaderReq, AddPartReq, AddLearnerReq, RemovePartReq, MemberChangeReq, CatchUpDataReq, GetLeaderReq, CreateCPRequest, DropCPRequest, BlockingSignRequest, GetLeaderPartsResp, CheckPeersReq, RebuildIndexRequest, CreateCPResp, ListClusterInfoResp, ListClusterInfoReq, KVGetRequest, KVGetResponse, KVPutRequest, KVRemoveRequest, InternalTxnRequest, GetValueRequest, GetValueResponse


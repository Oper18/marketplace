# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import market_pb2 as market__pb2


class GetCategoriesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetCats = channel.unary_unary(
                '/messenger.GetCategories/GetCats',
                request_serializer=market__pb2.CategoriesRequest.SerializeToString,
                response_deserializer=market__pb2.CategoriesResponse.FromString,
                )


class GetCategoriesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetCats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GetCategoriesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetCats': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCats,
                    request_deserializer=market__pb2.CategoriesRequest.FromString,
                    response_serializer=market__pb2.CategoriesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.GetCategories', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GetCategories(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetCats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.GetCategories/GetCats',
            market__pb2.CategoriesRequest.SerializeToString,
            market__pb2.CategoriesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ManageCategoryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ManageCats = channel.unary_unary(
                '/messenger.ManageCategory/ManageCats',
                request_serializer=market__pb2.CategoryManageRequest.SerializeToString,
                response_deserializer=market__pb2.CategoryItemResponse.FromString,
                )


class ManageCategoryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ManageCats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ManageCategoryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ManageCats': grpc.unary_unary_rpc_method_handler(
                    servicer.ManageCats,
                    request_deserializer=market__pb2.CategoryManageRequest.FromString,
                    response_serializer=market__pb2.CategoryItemResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.ManageCategory', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ManageCategory(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ManageCats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.ManageCategory/ManageCats',
            market__pb2.CategoryManageRequest.SerializeToString,
            market__pb2.CategoryItemResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class GetBrandsNamesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBrands = channel.unary_unary(
                '/messenger.GetBrandsNames/GetBrands',
                request_serializer=market__pb2.BrandRequest.SerializeToString,
                response_deserializer=market__pb2.BrandResponse.FromString,
                )


class GetBrandsNamesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetBrands(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GetBrandsNamesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetBrands': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBrands,
                    request_deserializer=market__pb2.BrandRequest.FromString,
                    response_serializer=market__pb2.BrandResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.GetBrandsNames', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GetBrandsNames(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetBrands(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.GetBrandsNames/GetBrands',
            market__pb2.BrandRequest.SerializeToString,
            market__pb2.BrandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ManageBrandsNamesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ManageBrands = channel.unary_unary(
                '/messenger.ManageBrandsNames/ManageBrands',
                request_serializer=market__pb2.BrandManageRequest.SerializeToString,
                response_deserializer=market__pb2.BrandItemResponse.FromString,
                )


class ManageBrandsNamesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ManageBrands(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ManageBrandsNamesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ManageBrands': grpc.unary_unary_rpc_method_handler(
                    servicer.ManageBrands,
                    request_deserializer=market__pb2.BrandManageRequest.FromString,
                    response_serializer=market__pb2.BrandItemResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.ManageBrandsNames', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ManageBrandsNames(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ManageBrands(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.ManageBrandsNames/ManageBrands',
            market__pb2.BrandManageRequest.SerializeToString,
            market__pb2.BrandItemResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class GetProductsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetProds = channel.unary_unary(
                '/messenger.GetProducts/GetProds',
                request_serializer=market__pb2.ProductRequest.SerializeToString,
                response_deserializer=market__pb2.ProductListResponse.FromString,
                )


class GetProductsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetProds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GetProductsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetProds': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProds,
                    request_deserializer=market__pb2.ProductRequest.FromString,
                    response_serializer=market__pb2.ProductListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.GetProducts', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GetProducts(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetProds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.GetProducts/GetProds',
            market__pb2.ProductRequest.SerializeToString,
            market__pb2.ProductListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ManageProductsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ManageProds = channel.unary_unary(
                '/messenger.ManageProducts/ManageProds',
                request_serializer=market__pb2.ProductManageRequest.SerializeToString,
                response_deserializer=market__pb2.ProductResponse.FromString,
                )


class ManageProductsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ManageProds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ManageProductsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ManageProds': grpc.unary_unary_rpc_method_handler(
                    servicer.ManageProds,
                    request_deserializer=market__pb2.ProductManageRequest.FromString,
                    response_serializer=market__pb2.ProductResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.ManageProducts', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ManageProducts(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ManageProds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.ManageProducts/ManageProds',
            market__pb2.ProductManageRequest.SerializeToString,
            market__pb2.ProductResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class GetProductsItemsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetProdItems = channel.unary_unary(
                '/messenger.GetProductsItems/GetProdItems',
                request_serializer=market__pb2.ProductItemsRequest.SerializeToString,
                response_deserializer=market__pb2.ProductItemsListResponse.FromString,
                )


class GetProductsItemsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetProdItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GetProductsItemsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetProdItems': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProdItems,
                    request_deserializer=market__pb2.ProductItemsRequest.FromString,
                    response_serializer=market__pb2.ProductItemsListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.GetProductsItems', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GetProductsItems(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetProdItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.GetProductsItems/GetProdItems',
            market__pb2.ProductItemsRequest.SerializeToString,
            market__pb2.ProductItemsListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class CreateProductsItemsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateProdItems = channel.unary_unary(
                '/messenger.CreateProductsItems/CreateProdItems',
                request_serializer=market__pb2.ProductItemsListCreateRequest.SerializeToString,
                response_deserializer=market__pb2.ProductItemsCreateResponse.FromString,
                )


class CreateProductsItemsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateProdItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CreateProductsItemsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateProdItems': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProdItems,
                    request_deserializer=market__pb2.ProductItemsListCreateRequest.FromString,
                    response_serializer=market__pb2.ProductItemsCreateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.CreateProductsItems', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CreateProductsItems(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateProdItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.CreateProductsItems/CreateProdItems',
            market__pb2.ProductItemsListCreateRequest.SerializeToString,
            market__pb2.ProductItemsCreateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class BuyProductItemStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.BuyProdItem = channel.unary_unary(
                '/messenger.BuyProductItem/BuyProdItem',
                request_serializer=market__pb2.ProductItemBuyRequest.SerializeToString,
                response_deserializer=market__pb2.ProductItemBuyResponse.FromString,
                )


class BuyProductItemServicer(object):
    """Missing associated documentation comment in .proto file."""

    def BuyProdItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BuyProductItemServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'BuyProdItem': grpc.unary_unary_rpc_method_handler(
                    servicer.BuyProdItem,
                    request_deserializer=market__pb2.ProductItemBuyRequest.FromString,
                    response_serializer=market__pb2.ProductItemBuyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.BuyProductItem', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BuyProductItem(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def BuyProdItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.BuyProductItem/BuyProdItem',
            market__pb2.ProductItemBuyRequest.SerializeToString,
            market__pb2.ProductItemBuyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class RemoveProductItemStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RemoveProdItem = channel.unary_unary(
                '/messenger.RemoveProductItem/RemoveProdItem',
                request_serializer=market__pb2.ProductItemRemoveRequest.SerializeToString,
                response_deserializer=market__pb2.ProductItemRemoveResponse.FromString,
                )


class RemoveProductItemServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RemoveProdItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RemoveProductItemServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RemoveProdItem': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveProdItem,
                    request_deserializer=market__pb2.ProductItemRemoveRequest.FromString,
                    response_serializer=market__pb2.ProductItemRemoveResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.RemoveProductItem', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RemoveProductItem(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RemoveProdItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.RemoveProductItem/RemoveProdItem',
            market__pb2.ProductItemRemoveRequest.SerializeToString,
            market__pb2.ProductItemRemoveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class RemoveProductStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RemoveProduct = channel.unary_unary(
                '/messenger.RemoveProduct/RemoveProduct',
                request_serializer=market__pb2.ProductRemoveRequest.SerializeToString,
                response_deserializer=market__pb2.ProductRemoveResponse.FromString,
                )


class RemoveProductServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RemoveProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RemoveProductServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RemoveProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveProduct,
                    request_deserializer=market__pb2.ProductRemoveRequest.FromString,
                    response_serializer=market__pb2.ProductRemoveResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.RemoveProduct', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RemoveProduct(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RemoveProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.RemoveProduct/RemoveProduct',
            market__pb2.ProductRemoveRequest.SerializeToString,
            market__pb2.ProductRemoveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ProductItemsStatStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProductItemsStat = channel.unary_unary(
                '/messenger.ProductItemsStat/ProductItemsStat',
                request_serializer=market__pb2.ProductItemsStatRequest.SerializeToString,
                response_deserializer=market__pb2.ProductItemsStatResponse.FromString,
                )


class ProductItemsStatServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ProductItemsStat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProductItemsStatServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ProductItemsStat': grpc.unary_unary_rpc_method_handler(
                    servicer.ProductItemsStat,
                    request_deserializer=market__pb2.ProductItemsStatRequest.FromString,
                    response_serializer=market__pb2.ProductItemsStatResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messenger.ProductItemsStat', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ProductItemsStat(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ProductItemsStat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messenger.ProductItemsStat/ProductItemsStat',
            market__pb2.ProductItemsStatRequest.SerializeToString,
            market__pb2.ProductItemsStatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

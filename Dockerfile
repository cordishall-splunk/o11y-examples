FROM nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Custom lines Adding the SignalFx Auto-Instrumentation to the image:

# First install the package. This example downloads the latest version
# alternatively download a specific version or use a local copy.
ARG TRACER_VERSION=0.1.3
ADD https://github.com/signalfx/signalfx-dotnet-tracing/releases/download/v${TRACER_VERSION}/signalfx-dotnet-tracing_${TRACER_VERSION}_amd64.deb .
RUN dpkg -i signalfx-dotnet-tracing_${TRACER_VERSION}_amd64.deb
RUN rm -rf /signalfx-package

# Prepare the log directory (useful for local tests).
RUN mkdir -p /var/log/signalfx/dotnet && \
    chmod a+rwx /var/log/signalfx/dotnet

# Set the required environment variables. In the case of Azure Functions more
# can be set either here or on the application settings.
ENV CORECLR_ENABLE_PROFILING=1 \
    CORECLR_PROFILER='{B4C89B0F-9908-4F73-9F59-0D77C5A06874}' \
    CORECLR_PROFILER_PATH=/opt/signalfx-dotnet-tracing/SignalFx.Tracing.ClrProfiler.Native.so \
    SIGNALFX_INTEGRATIONS=/opt/signalfx-dotnet-tracing/integrations.json \
    SIGNALFX_DOTNET_TRACER_HOME=/opt/signalfx-dotnet-tracing \
    SIGNALFX_TRACE_DEBUG=true \
    SIGNALFX_TRACE_DOMAIN_NEUTRAL_INSTRUMENTATION=true \
    SIGNALFX_STDOUT_LOG_ENABLED=true \
    SIGNALFX_ENDPOINT_URL=http://127.0.0.1:9080/v1/trace

#link SFX tracing log directory to stdout
RUN ln -s /dev/stdout /var/log/signalfx/dotnet

# End of SignalFx customization.

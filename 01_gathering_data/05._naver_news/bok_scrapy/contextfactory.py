from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory


class LegacyConnectContextFactory(ScrapyClientContextFactory):

    def getContext(self, hostname=None, port=None):
        ctx = self.getCertificateOptions().getContext()
        ctx.set_options(0x4)
        return ctx

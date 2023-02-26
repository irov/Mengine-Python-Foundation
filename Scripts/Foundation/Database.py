class Database(object):
    def __init__(self):
        self.records = []
        self.orms = []
        self.legends = {}
        self.indexer = None
        self.indexer_cache = {}
        pass

    def addRecord(self, **record):
        self.records.append(record)
        pass

    def getRecords(self):
        return self.records
        pass

    def getRecord(self, rowType, value):
        for record in self.records:
            rowValue = record.get(rowType)

            if rowValue is None:
                continue
                pass

            if rowValue == value:
                return record
                pass
            pass

        return None
        pass

    def makeIndexer(self, indexer):
        self.indexer = indexer

        for orm in self.orms:
            indexer_value = getattr(orm, indexer)

            if indexer_value not in self.indexer_cache:
                self.indexer_cache[indexer_value] = []
                pass

            self.indexer_cache[indexer_value].append(orm)
            pass
        pass

    def getIndexer(self):
        return self.indexer
        pass

    def selectIndexerORMs(self, indexer):
        return self.indexer_cache.get(indexer, None)
        pass

    def setLegends(self, **legends):
        self.legends = legends
        pass

    def getLegends(self):
        return self.legends
        pass

    def filterRecord(self, rowType, value):
        records = []
        for record in self.records:
            rowValue = record.get(rowType)

            if rowValue is None:
                continue
                pass

            if rowValue == value:
                records.append(record)
                pass
            pass

        return records
        pass

    def addORM(self, orm):
        self.orms.append(orm)
        pass

    def getORMs(self):
        return self.orms
        pass
    pass
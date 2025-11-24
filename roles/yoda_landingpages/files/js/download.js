let downloadZip
const downloadButton = document.getElementById('downloadZip')
try {
  downloadZip = (await import('../../static/lib/client-zip-2.5.0.js')).downloadZip
  downloadButton.classList.remove('invisible')
} catch (error) {
  console.error('Download zip import failed:', error)
}

const openAccessLink = document.getElementById('viewContents').href
const randomId = document.getElementById('viewContents').getAttribute('data-random-id')

document.body.addEventListener('click', async function (event) {
  if (event.target.matches('a#downloadZip')) {
    event.preventDefault()
    downloadButton.classList.add('disabled')
    downloadButton.innerText = 'Downloading...'

    const manifestUrl = `./${randomId}-manifest.json`
    try {
      const response = await fetch(manifestUrl)
      if (!response.ok) throw new Error(`Error: ${response.status}`)
      const entries = await response.json()

      const downloadEntries = entries.reduce((acc, entry) => {
        if (entry.name.endsWith('/')) {
          acc.push({ name: entry.name })
        } else {
          acc.push({
            url: `${openAccessLink}/${entry.name}`,
            name: entry.name
          })
        }
        return acc
      }, [])

      if (downloadEntries.length) {
        await downloadEntriesAsZip(downloadEntries)
        console.log('ZIP download triggered.')
      }
    } catch (error) {
      console.error('ZIP failed:', error)
    } finally {
      downloadButton.innerText = 'Download as zip'
      downloadButton.classList.remove('disabled')
    }
  }
})

async function downloadEntriesAsZip (entries) {
  const MAX_PARALLEL = 2

  const results = new Array(entries.length)
  let cursor = 0

  async function worker () {
    while (cursor < entries.length) {
      const i = cursor++
      const { url, name } = entries[i]

      if (!url) { 
        results[i] = { name }
        continue
      }

      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`Failed to fetch ${url}: ${response.status} ${response.statusText}`)
      }
      const blob = await response.blob()   // blocks until finished, this prevent more than MAX_PARALLEL threads running

      results[i] = { name, lastModified: Date.now(), input: blob }
    }
  }

  const workers = Array.from({ length: Math.min(MAX_PARALLEL, entries.length) }, worker)
  await Promise.all(workers)

  const zipBlob = await downloadZip(results).blob()
  const downloadLink = document.createElement('a')
  downloadLink.href = URL.createObjectURL(zipBlob)
  downloadLink.download = 'download.zip'

  document.body.appendChild(downloadLink)
  downloadLink.click()
  document.body.removeChild(downloadLink)
  URL.revokeObjectURL(downloadLink.href)
}
